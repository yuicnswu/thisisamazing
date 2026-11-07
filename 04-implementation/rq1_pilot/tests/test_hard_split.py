import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attributes import Need, support_label  # noqa: E402
from data import Listing  # noqa: E402
import hard_split as H  # noqa: E402


def _listing():
    return Listing("B0TEST", "Calm Gel Cleanser for Dry Skin, Paraben-Free, 6 oz",
                   ["Gentle daily gel cleanser made for dry skin.", "Paraben-free and sulfate-free formula."],
                   ["A soothing gel. Use morning and night."],
                   {"Skin Type": "Dry", "Material Type Free": "Paraben Free", "Item Form": "Gel"}, "Calm", "test")


def test_conj_label():
    assert H.conj_label(["entailed", "entailed"]) == "entailed"
    assert H.conj_label(["entailed", "unresolved"]) == "unresolved"
    assert H.conj_label(["unresolved", "contradicted"]) == "contradicted"
    assert H.conj_label(["conflicting", "entailed"]) == "contradicted"


def test_build_conj_edits_only_the_target_constraint():
    rows = H.build_conj([_listing()], random.Random(0))
    assert {r["variant"] for r in rows} >= {"original", "remove"}
    for r in rows:
        l = H._load_listing(r["listing"])
        labs = [support_label(Need(*n), l.visible_text()) for n in r["needs"]]
        assert labs[1] == "entailed"  # the non-target constraint is untouched
        assert H.conj_label(labs) == r["label"]
        assert len({n[0] for n in r["needs"]}) == 2  # two different attributes


def test_joint_need_text_names_every_constraint():
    t = H.JointNeed([Need("skin_type", "dry"), Need("free_from", "paraben")]).text()
    assert "dry skin" in t and "paraben-free" in t and "All of these must hold" in t


def test_apply_replaces_only_the_given_passages():
    l = _listing()
    passages = [("b0", "Gentle daily gel cleanser made for dry skin.")]
    out = H._apply(l, passages, ["Gentle daily gel cleanser made for parched, thirsty complexions."])
    assert "parched" in out.bullets[0]
    assert out.bullets[1] == l.bullets[1] and out.title == l.title
