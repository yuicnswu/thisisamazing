"""Step 4b. Transformer-based scaling: pretrained sentence encoder + linear heads, compared with TF-IDF.

TF-IDF logistic regression (scale.py) is a strong but dated baseline. Here every review is encoded with a
pretrained transformer sentence encoder (default BAAI/bge-small-en-v1.5; Xiao et al. 2023) and an L2
logistic-regression head is fitted per target on the train labels (C by 5-fold CV), the light-weight
transfer recipe of SetFit-style classifiers (Tunstall et al. 2022) without contrastive fine-tuning.
For each target three predictors are compared: tfidf (scale.py), emb, and ens (mean of the two).
The predictor used downstream is chosen per target by cross-validated average precision on the TRAIN
sample only, so the calib sample stays untouched for PPI. PPI++ remains valid for any predictor; a better
one only narrows the intervals, which is reported (mean 95% half-width over targets).

Needs: pip install sentence-transformers  (downloads the encoder from Hugging Face on first run).
Usage: python scale_embed.py <source> [--model BAAI/bge-small-en-v1.5] [--batch 256]
Run after scale.py. Writes outputs/<source>/embeddings.npy, predictions_emb.parquet, scale_embed_eval.json.
Then: PREDICTIONS=predictions_emb.parquet python analyze.py <source>
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_predict

from scale import HERE, MIN_POSITIVES, gold_name, load_labels, ppi_mean, targets


def encode(texts, model_name, batch):
    from sentence_transformers import SentenceTransformer
    import torch
    dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    m = SentenceTransformer(model_name, device=dev)
    m.max_seq_length = 256
    return m.encode(texts, batch_size=batch, show_progress_bar=True, normalize_embeddings=True, convert_to_numpy=True).astype(np.float32)


KEY = ["author_id", "product_id", "date"]


def embed_keyed(source, model_name="BAAI/bge-small-en-v1.5", batch=256):
    """Encode on another machine and save with natural keys, so the embeddings can be joined to a
    reviews.parquet whose review_ids were numbered by a different parse run."""
    out = os.path.join(HERE, "outputs", source)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"), columns=KEY + ["title", "text"])
    E = encode((df.title.fillna("") + " . " + df.text).tolist(), model_name, batch)
    np.save(os.path.join(out, "embeddings_keyed.npy"), E.astype(np.float16))
    df[KEY].to_parquet(os.path.join(out, "embedding_keys.parquet"), index=False)


def load_keyed(out, df):
    E = np.load(os.path.join(out, "embeddings_keyed.npy")).astype(np.float32)
    k = pd.read_parquet(os.path.join(out, "embedding_keys.parquet")).assign(_row=np.arange(len(E)))
    k = k.drop_duplicates(KEY)
    m = df[KEY].merge(k, on=KEY, how="left")
    hit = m._row.notna().values
    X = np.zeros((len(df), E.shape[1]), np.float32)
    X[hit] = E[m._row[hit].astype(int).values]
    print(f"joined embeddings for {hit.mean():.4%} of reviews", flush=True)
    return X


def main(source, model_name="BAAI/bge-small-en-v1.5", batch=256, encoder=None):
    out = os.path.join(HERE, "outputs", source)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"), columns=["review_id", "title", "text"] + KEY)
    epath = os.path.join(out, "embeddings.npy")
    if os.path.exists(os.path.join(out, "embeddings_keyed.npy")):
        E = load_keyed(out, df)
    elif os.path.exists(epath):
        E = np.load(epath)
    else:
        texts = (df.title.fillna("") + " . " + df.text).tolist()
        E = (encoder or (lambda t: encode(t, model_name, batch)))(texts)
        np.save(epath, E)
    idx = {r: i for i, r in enumerate(df.review_id)}
    tf = pd.read_parquet(os.path.join(out, "predictions.parquet")).set_index("review_id").loc[df.review_id]
    tr, ca = load_labels(out, "train"), load_labels(out, "calib", gold_name(out))
    Xtr, Xca = E[[idx[r] for r in tr.review_id]], E[[idx[r] for r in ca.review_id]]
    tf_oof = pd.read_parquet(os.path.join(out, "predictions_train_oof.parquet")).set_index("review_id").loc[tr.review_id]
    cv = StratifiedKFold(5, shuffle=True, random_state=0)
    preds = {"review_id": df.review_id.values}
    ev = {}
    for t in targets():
        y = tr[t].values
        if t not in tf.columns or y.sum() < MIN_POSITIVES or (len(y) - y.sum()) < MIN_POSITIVES:
            continue
        gs = GridSearchCV(LogisticRegression(max_iter=3000), {"C": [0.25, 1, 4, 16]}, scoring="average_precision", cv=cv, n_jobs=4)
        gs.fit(Xtr, y)
        emb_oof = cross_val_predict(gs.best_estimator_, Xtr, y, cv=cv, method="predict_proba")[:, 1]
        tf_o = tf_oof[t].values
        cand_cv = {"tfidf": average_precision_score(y, tf_o), "emb": average_precision_score(y, emb_oof),
                   "ens": average_precision_score(y, (emb_oof + tf_o) / 2)}
        p_emb = gs.best_estimator_.predict_proba(E)[:, 1].astype(np.float32)
        p_all = {"tfidf": tf[t].values, "emb": p_emb, "ens": (p_emb + tf[t].values) / 2}
        pick = max(cand_cv, key=cand_cv.get)
        preds[t] = p_all[pick].astype(np.float32)
        yc = ca[t].values
        e = {"pick": pick, "cv_avg_precision": {k: round(float(v), 3) for k, v in cand_cv.items()}}
        for k, p in p_all.items():
            pc = p[[idx[r] for r in ca.review_id]]
            r_ = ppi_mean(yc, pc, p)
            e[k] = {"calib_auroc": round(roc_auc_score(yc, pc), 3) if 0 < yc.sum() < len(yc) else None,
                    "ppi_halfwidth": round(1.96 * r_["se"], 5)}
        ev[t] = e
    pd.DataFrame(preds).to_parquet(os.path.join(out, "predictions_emb.parquet"), index=False)
    summ = {k: float(np.mean([e[k]["ppi_halfwidth"] for e in ev.values()])) for k in ("tfidf", "emb", "ens")}
    summ["picked"] = float(np.mean([e[e["pick"]]["ppi_halfwidth"] for e in ev.values()]))
    auc = {k: float(np.nanmean([e[k]["calib_auroc"] or np.nan for e in ev.values()])) for k in ("tfidf", "emb", "ens")}
    res = {"encoder": model_name, "mean_ppi_halfwidth": summ, "mean_calib_auroc": auc,
           "picks": pd.Series([e["pick"] for e in ev.values()]).value_counts().to_dict(), "per_target": ev}
    with open(os.path.join(out, "scale_embed_eval.json"), "w") as f:
        json.dump(res, f, indent=2)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("--model", default="BAAI/bge-small-en-v1.5"); ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--encode-only", action="store_true", help="only write embeddings_keyed.npy + embedding_keys.parquet")
    a = ap.parse_args()
    if a.encode_only:
        embed_keyed(a.source, a.model, a.batch)
        raise SystemExit
    r = main(a.source, a.model, a.batch)
    print(json.dumps({k: v for k, v in r.items() if k != "per_target"}, indent=2))
