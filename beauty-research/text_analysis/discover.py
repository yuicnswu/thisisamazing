"""Step 2. Unsupervised aspect discovery, used to fix the aspect taxonomy before any labelling.

(a) NMF topic model on TF-IDF (unigrams + bigrams) over a random sample of reviews.
(b) Weighted log-odds ratio with an informative Dirichlet prior (Monroe, Colaresi & Quinn, 2008):
    which words separate low-star (1-2) from high-star (4-5) reviews, with z-scores.

Usage: python discover.py <source> [--sample 200000] [--k 30]
Writes outputs/<source>/topics.json, outputs/<source>/logodds.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, CountVectorizer, TfidfVectorizer

HERE = os.path.dirname(os.path.abspath(__file__))

# Generic evaluative words and title boilerplate ("Five Stars"). Without them NMF topics are
# sentiment clusters ("great", "love") instead of aspects. Used for topics only, not for log-odds.
GENERIC = {"great", "good", "love", "loved", "loves", "like", "nice", "really", "product", "products", "stars",
           "star", "five", "four", "three", "excellent", "awesome", "amazing", "perfect", "best", "just", "ok",
           "okay", "bad", "terrible", "horrible", "wonderful", "fantastic", "recommend", "highly", "item",
           "stuff", "buy", "bought", "purchase", "purchased", "use", "used", "using", "work", "works", "worked",
           "don", "didn", "doesn", "did", "does", "ve", "got", "get", "would", "will", "one", "well", "much",
           "beautiful", "cute", "pretty", "happy", "disappointed", "definitely", "absolutely", "super", "lot"}
GENERIC |= {"don't", "didn't", "doesn't", "isn't", "wasn't", "won't", "can't", "i'm", "it's", "i've", "i'd", "i'll", "you'll", "that's"}
STOP = list(ENGLISH_STOP_WORDS | GENERIC)
TOKEN = r"(?u)\b[a-z]+(?:'[a-z]+)?\b"   # same tokens as parse.tokens: keeps contractions such as "didn't" whole


def nmf_topics(texts, k=30, seed=0, n_top=15):
    vec = TfidfVectorizer(stop_words=STOP, token_pattern=TOKEN, ngram_range=(1, 2), min_df=20, max_df=0.4,
                          max_features=40000, sublinear_tf=True)
    X = vec.fit_transform(texts)
    model = NMF(n_components=k, init="nndsvda", random_state=seed, max_iter=400)
    W = model.fit_transform(X)
    terms = np.array(vec.get_feature_names_out())
    share = (W.argmax(1)[:, None] == np.arange(k)).mean(0)
    return [{"topic": t, "share_dominant": round(float(share[t]), 4),
             "top_terms": terms[np.argsort(-model.components_[t])[:n_top]].tolist()} for t in range(k)]


def weighted_log_odds(texts_a, texts_b, prior_texts, min_count=50, n_top=40):
    """Monroe et al. (2008) eq. 16-22: delta_w with Dirichlet prior from the pooled corpus; z = delta / sd."""
    vec = CountVectorizer(stop_words="english", token_pattern=TOKEN, ngram_range=(1, 2), min_df=min_count, max_features=50000)
    vec.fit(prior_texts)
    ya = np.asarray(vec.transform(texts_a).sum(0)).ravel().astype(float)
    yb = np.asarray(vec.transform(texts_b).sum(0)).ravel().astype(float)
    alpha = np.asarray(vec.transform(prior_texts).sum(0)).ravel().astype(float)
    alpha = alpha / alpha.sum() * 10000.0          # prior strength a0 = 10,000 pseudo-counts
    na, nb, a0 = ya.sum(), yb.sum(), alpha.sum()
    la = np.log((ya + alpha) / (na + a0 - ya - alpha))
    lb = np.log((yb + alpha) / (nb + a0 - yb - alpha))
    delta = la - lb
    z = delta / np.sqrt(1 / (ya + alpha) + 1 / (yb + alpha))
    terms = np.array(vec.get_feature_names_out())
    order = np.argsort(-z)
    pick = lambda idx: [{"term": terms[i], "z": round(float(z[i]), 1), "count_a": int(ya[i]), "count_b": int(yb[i])} for i in idx]
    return {"a_over_b": pick(order[:n_top]), "b_over_a": pick(order[::-1][:n_top])}


def main(source, sample=200000, k=30, seed=0):
    out = os.path.join(HERE, "outputs", source)
    df = pd.read_parquet(os.path.join(out, "reviews.parquet"), columns=["title", "text", "rating"])
    df = df.sample(n=min(sample, len(df)), random_state=seed)
    full = (df.title + ". " + df.text).tolist()
    topics = nmf_topics(df.text.tolist(), k=k, seed=seed)
    with open(os.path.join(out, "topics.json"), "w") as f:
        json.dump(topics, f, indent=2)
    low = df.rating <= 2
    high = df.rating >= 4
    lo = weighted_log_odds([t for t, m in zip(full, low) if m], [t for t, m in zip(full, high) if m], full)
    with open(os.path.join(out, "logodds.json"), "w") as f:
        json.dump({"a": "rating<=2", "b": "rating>=4", **lo}, f, indent=2)
    return topics, lo


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("--sample", type=int, default=200000); ap.add_argument("--k", type=int, default=30)
    a = ap.parse_args()
    topics, lo = main(a.source, a.sample, a.k)
    for t in topics:
        print(t["topic"], t["share_dominant"], ", ".join(t["top_terms"][:10]))
    print("LOW:", ", ".join(x["term"] for x in lo["a_over_b"][:40]))
    print("HIGH:", ", ".join(x["term"] for x in lo["b_over_a"][:40]))
