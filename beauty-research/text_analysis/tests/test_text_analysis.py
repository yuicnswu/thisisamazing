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
