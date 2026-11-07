import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from label import quote_ok  # noqa: E402
from parse import clean_text  # noqa: E402
from scale import ppi_mean  # noqa: E402


def test_quote_ok_is_case_and_space_insensitive():
    assert quote_ok("Smells  GREAT.", "It smells great. Love it")
    assert not quote_ok("smells amazing", "It smells great")
    assert not quote_ok("", "anything")


def test_clean_text_strips_tags_and_entities():
    assert clean_text("Nice<br />product &amp; scent") == "Nice product & scent"
    assert clean_text("don\u2019t \u201cwow\u201d") == "don't \"wow\""


def test_ppi_is_unbiased_with_a_biased_classifier():
    rng = np.random.default_rng(0)
    N, n, p = 200000, 2000, 0.2
    y_all = rng.random(N) < p
    f_all = np.clip(0.5 * y_all + 0.25 + rng.normal(0, 0.1, N), 0, 1)   # biased upwards
    lab = rng.choice(N, n, replace=False)
    r = ppi_mean(y_all[lab].astype(float), f_all[lab], f_all)
    assert abs(f_all.mean() - p) > 0.1                 # naive classifier mean is far off
    assert r["lo"] <= y_all.mean() <= r["hi"]          # PPI interval covers the truth
    assert r["hi"] - r["lo"] < 2 * 1.96 * np.sqrt(p * (1 - p) / n)   # and is narrower than labels alone


def test_ppi_coverage_close_to_nominal():
    rng = np.random.default_rng(1)
    hits = 0
    for _ in range(300):
        y = rng.random(20000) < 0.1
        f = np.clip(0.6 * y + rng.normal(0.1, 0.15, 20000), 0, 1)
        lab = rng.choice(20000, 500, replace=False)
        r = ppi_mean(y[lab].astype(float), f[lab], f)
        hits += r["lo"] <= y.mean() <= r["hi"]
    assert hits / 300 > 0.9


def _toy_sephora(n=3000, seed=0):
    import pandas as pd
    rng = np.random.default_rng(seed)
    days = pd.Timestamp("2020-01-01", tz="UTC") + pd.to_timedelta(rng.integers(0, 400, n), unit="D")
    return pd.DataFrame({"review_id": [f"r{i}" for i in range(n)], "product_id": rng.integers(0, 40, n).astype(str),
                         "author_id": rng.integers(0, 600, n).astype(str), "rating": rng.integers(1, 6, n).astype(float),
                         "date": days, "skin_type": rng.choice(["dry", "oily", None], n), "category": rng.choice(["a", "b"], n),
                         "is_recommended": (rng.random(n) < 0.8).astype(float)})


def test_rq3_features_use_only_earlier_days():
    from rq3_temporal import build_features
    df = _toy_sephora()
    f1 = build_features(df, "is_recommended").set_index("review_id")
    last = df.date.max()
    df2 = df.copy()
    flip = df2.date == last                       # change every target on the last day
    df2.loc[flip, "is_recommended"] = 1 - df2.loc[flip, "is_recommended"]
    df2.loc[flip, "rating"] = 6 - df2.loc[flip, "rating"]
    f2 = build_features(df2, "is_recommended").set_index("review_id")
    cols = ["prod_rate", "prod_skin_rate", "auth_rate", "auth_cat_rate", "prod_mean_rating", "auth_mean_rating", "cat_rate"]
    pd_ = __import__("pandas")
    pd_.testing.assert_frame_equal(f1.loc[:, cols], f2.loc[f1.index, cols])   # no row sees the last day's outcomes
    first = f1.sort_values("date").groupby("product_id").head(1)
    assert (first.prod_n == 0).all()


def test_entail_contrast_set_has_known_negatives():
    from entail import contrast_set
    recs = [{"review_id": "x", "labels": [{"a": "scent", "p": "pos", "q": "smells great"},
                                          {"a": "texture", "p": "neg", "q": "too sticky"}]}]
    items = contrast_set(recs, {"x": "smells great but too sticky"}, n=5)
    kinds = sorted(i["kind"] for i in items)
    assert kinds.count("orig") == 2 and kinds.count("flip") == 2 and kinds.count("wrong") == 2
    flip = [i for i in items if i["kind"] == "flip" and i["a"] == "scent"][0]
    assert flip["p"] == "neg"
    swap = [i for i in items if i["kind"] == "swap"]
    assert all(i["a"] not in ("scent", "texture", "overall") for i in swap)
