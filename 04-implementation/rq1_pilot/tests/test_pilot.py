import os
import random
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import llm  # noqa: E402
from attributes import Need, details_values, find_values, support_label  # noqa: E402
from data import Listing  # noqa: E402
from edits import LABEL, add_prior, contradict, remove, vague  # noqa: E402
from ltt import binom_pvalue, evaluate, ltt_threshold, summarize  # noqa: E402
from matchers import keyword_rule, rule_on_extraction  # noqa: E402
from edits import Item  # noqa: E402


# ---- attributes -------------------------------------------------------------------------------
@pytest.mark.parametrize("text,attr,expected", [
    ("For Oily, Combination, Dry skin", "skin_type", {"oily", "combination", "dry"}),
    ("great for dry and sensitive skin", "skin_type", {"dry", "sensitive"}),
    ("suitable for all skin types", "skin_type", {"all"}),
    ("dries quickly, dry hands", "skin_type", set()),
    ("for fine, thin hair", "hair_type", {"fine"}),
    ("Unscented roll-on", "scent", {"unscented"}),
    ("oil-free gel moisturizer", "free_from", {"oil"}),
    ("oil-free gel moisturizer", "item_form", {"gel"}),
    ("paraben-free, sulfate free", "free_from", {"paraben", "sulfate"}),
])
def test_find_values(text, attr, expected):
    assert set(find_values(attr, text)) == expected


def test_details_values():
    assert details_values("skin_type", {"Skin Type": "Oily, Combination, Dry"}) == {"oily", "combination", "dry"}
    assert details_values("skin_type", {"Skin Type": "All"}) == {"all"}
    assert details_values("scent", {"Scent": "Fragrance Free"}) == {"unscented"}
    assert details_values("free_from", {"Material Type Free": "Paraben Free, Sulfate Free"}) == {"paraben", "sulfate"}
    assert details_values("hair_type", {}) == set()


@pytest.mark.parametrize("need,text,label", [
    (Need("skin_type", "dry"), "A rich cream for dry skin.", "entailed"),
    (Need("skin_type", "dry"), "Gentle on all skin types.", "entailed"),          # §12.1 'all' rule
    (Need("skin_type", "dry"), "Mattifying gel for oily skin.", "contradicted"),
    (Need("skin_type", "dry"), "For dry skin and oily skin.", "conflicting"),
    (Need("skin_type", "dry"), "Hydrating, moisturizing face cream.", "unresolved"),  # implied is not stated
    (Need("free_from", "paraben"), "Paraben-free formula.", "entailed"),
    (Need("free_from", "paraben"), "A paraben-based preservative system.", "contradicted"),
    (Need("free_from", "paraben"), "Natural formula.", "unresolved"),                # absence is never contradiction
    (Need("scent", "unscented"), "Lavender scented lotion.", "contradicted"),
])
def test_support_label(need, text, label):
    assert support_label(need, text) == label


# ---- edits ------------------------------------------------------------------------------------
def _listing():
    return Listing("A1", "Acme Daily Cream for Dry Skin, 2 oz", ["Made for dry skin. Absorbs fast.", "Paraben-free."],
                   ["Our cream soothes dry skin overnight."], {"Skin Type": "Dry"}, "Acme")


def test_render_hides_details():
    assert "Skin Type" not in _listing().render()


def test_remove_deletes_every_statement():
    need = Need("skin_type", "dry")
    l2 = remove(_listing(), "skin_type")
    assert support_label(need, l2.visible_text()) == LABEL["remove"]
    assert "Absorbs fast." in l2.visible_text()          # unrelated sentence kept
    assert "Paraben-free." in l2.visible_text()


def test_vague_and_contradict():
    need = Need("skin_type", "dry")
    assert support_label(need, vague(_listing(), "skin_type", "dry").visible_text()) == "unresolved"
    c = contradict(_listing(), "skin_type", "dry", random.Random(0))
    assert support_label(need, c.visible_text()) == "contradicted"
    assert "oily skin" in c.visible_text().lower()


def test_add_prior_swaps_brand_and_adds_hype():
    l2 = add_prior(remove(_listing(), "skin_type"), "skin_type")
    assert l2.store == "CeraVe" and "Acme" not in l2.render()
    assert "dermatologist" in l2.bullets[0]
    assert support_label(Need("skin_type", "dry"), l2.visible_text()) == "unresolved"


# ---- matchers ---------------------------------------------------------------------------------
def test_rule_on_extraction():
    n = Need("skin_type", "dry")
    assert rule_on_extraction(n, {"skin_types": ["dry"]}) == "recommend"
    assert rule_on_extraction(n, {"skin_types": ["all"]}) == "recommend"
    assert rule_on_extraction(n, {"skin_types": ["oily"]}) == "reject"
    assert rule_on_extraction(n, {"skin_types": []}) == "abstain"
    assert rule_on_extraction(Need("free_from", "paraben"), {"free_from": [], "contains": ["paraben"]}) == "reject"
    assert rule_on_extraction(Need("scent", "unscented"), {"scent": "lavender"}) == "reject"


def test_keyword_rule_decisions():
    l = _listing()
    items = [Item("a", "A1", "original", Need("skin_type", "dry"), "entailed", l),
             Item("b", "A1", "remove", Need("skin_type", "dry"), "unresolved", remove(l, "skin_type"))]
    out = keyword_rule(items)
    assert out["a"]["decision"] == "recommend" and out["b"]["decision"] == "abstain"


def test_parse_json_handles_fences_and_prose():
    assert llm.parse_json('Sure:\n```json\n[{"id": "x"}]\n```') == [{"id": "x"}]
    assert llm.parse_json('here [{"id": 1}] done') == [{"id": 1}]
    with pytest.raises(ValueError):
        llm.parse_json("no json")


def test_llm_cache(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(llm, "CACHE", str(tmp_path / "c.jsonl"))
    monkeypatch.setattr(llm, "_mem", None)
    monkeypatch.setattr(llm, "_claude", lambda m, s, p: calls.append(p) or "out")
    assert llm.complete("claude", "m", "s", "p") == "out"
    assert llm.complete("claude", "m", "s", "p") == "out"
    assert len(calls) == 1


# ---- Learn-then-Test --------------------------------------------------------------------------
def test_binom_pvalue():
    assert binom_pvalue(0, 0, 0.05) == 1.0
    assert binom_pvalue(0, 100, 0.05) < 0.01
    assert binom_pvalue(10, 100, 0.05) > 0.9


def test_ltt_threshold_separable():
    scores = np.r_[np.linspace(0.6, 1, 200), np.linspace(0, 0.4, 200)]
    uns = np.r_[np.zeros(200, bool), np.ones(200, bool)]
    lam = ltt_threshold(scores, uns, alpha=0.05, delta=0.1)
    assert lam is not None and 0.4 < lam <= 0.6


def test_ltt_returns_none_when_risk_too_high():
    rng = np.random.default_rng(0)
    assert ltt_threshold(rng.random(200), rng.random(200) < 0.5, alpha=0.05) is None


def test_ltt_validity_on_noisy_scores():
    """Risk control: over many calibration draws, test URR exceeds alpha in at most ~delta of them."""
    rng = np.random.default_rng(1)
    n = 2000
    uns = rng.random(n) < 0.3
    scores = np.clip(np.where(uns, 0.4, 0.6) + rng.normal(0, 0.2, n), 0, 1)
    rows = evaluate(scores, uns, np.arange(n), alpha=0.1, delta=0.1, n_splits=200)
    s = summarize(rows, 0.1)
    assert s["violation_rate"] <= 0.15
    assert s["coverage"][0] > 0


def test_prompt_hides_variant_label_and_details():
    from matchers import _case
    it = Item("A1:skin_type:dry:contradict", "A1", "contradict", Need("skin_type", "dry"), "contradicted", _listing())
    shown = _case(it)
    for leak in ("contradict", "contradicted", "A1", "skin_type", "Skin Type"):
        assert leak not in shown


# ---- neuro-symbolic verifier and Algorithm 1 --------------------------------------------------
def test_nesy_certificate_grounds_and_types_quotes():
    from matchers import _norm_text, certificate, contradict_terms, support_terms, tiered
    page = _norm_text(_listing().render())
    dry = Need("skin_type", "dry")
    assert certificate("Made for dry skin.", page, support_terms(dry)) == (True, True)
    assert certificate("Absorbs fast.", page, support_terms(dry)) == (True, False)       # verbatim, wrong value
    assert certificate("Ideal for dry skin", page, support_terms(dry)) == (False, False)  # not in the listing
    assert certificate("", page, support_terms(dry)) == (False, False)
    assert "oily skin" in contradict_terms(dry)
    assert "fragrance" not in contradict_terms(Need("scent", "unscented"))  # "fragrance-free" must not contradict
    assert tiered(0.0, True, True) > tiered(1.0, True, False) > tiered(1.0, False, False)


def test_decide_reject_takes_precedence():
    from conformal import ABS, REC, REJ, decide
    assert list(decide([0.9, 0.9, 0.1], [0.9, 0.1, 0.1], lam=0.5, tau=0.8)) == [REJ, REC, ABS]


def test_fixed_sequence_stops_at_first_failure():
    from conformal import fixed_sequence
    e = np.r_[np.full(60, 0.9), np.full(60, 0.5), np.full(60, 0.1)]
    unsup = np.r_[np.zeros(60, bool), np.ones(60, bool), np.zeros(60, bool)]
    cert = fixed_sequence(e, np.zeros(180), unsup, np.ones(180, bool), [0.9, 0.5, 0.1], np.inf, 0.1, 0.1, 0.1)
    assert [lam for lam, _ in cert] == [0.9]   # 0.5 fails, so 0.1 is never tested even though it would pass


def test_clopper_pearson():
    from conformal import clopper_pearson
    lo, hi = clopper_pearson(0, 29)
    assert lo == 0 and abs(hi - 0.1194) < 1e-3
    assert clopper_pearson(5, 0) == (0.0, 1.0)


def test_algorithm1_controls_urr_on_synthetic_products():
    from conformal import algorithm1, summarize1
    rng = np.random.default_rng(0)
    n_prod = 1500
    groups = np.repeat(np.arange(n_prod), 2)
    unsup = rng.random(2 * n_prod) < 0.6
    e = np.clip(np.where(unsup, 0.35, 0.65) + rng.normal(0, 0.15, 2 * n_prod), 0, 1)
    rows = algorithm1(e, np.zeros_like(e), unsup, np.ones_like(unsup), groups, alpha=0.1, delta=0.1, n_splits=60)
    s = summarize1(rows, 0.1, 0.1)
    assert s["no_threshold_rate"] < 0.5 and s["coverage"][0] > 0.05
    assert s["violation_rate"] <= 0.2   # theory: <= delta (0.1) for the population; test-set noise adds a little
