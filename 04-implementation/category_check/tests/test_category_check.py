import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from category_check import appliance_mentions, beauty_mentions, certify_prob, min_recommended  # noqa: E402


def test_certify_prob_monotone_in_n_and_zero_when_true_risk_is_alpha():
    assert certify_prob(50, 0.02, 0.10, 0.10) < certify_prob(150, 0.02, 0.10, 0.10)
    # When the true URR equals alpha the test is valid: certification probability <= delta.
    for n in (30, 100, 400):
        assert certify_prob(n, 0.10, 0.10, 0.10) <= 0.10 + 1e-9


def test_min_recommended_matches_zero_failure_floor():
    # With r = 0, the smallest n is the zero-failure floor ceil(log delta / log(1 - alpha)) = 22 at alpha = delta = 0.1.
    assert min_recommended(0.0, 0.10, 0.10, 0.9) == 22
    assert min_recommended(0.02, 0.05, 0.10, 0.9) > min_recommended(0.02, 0.10, 0.10, 0.9)


def test_appliance_detector():
    assert appliance_mentions("Fits my Samsung fridge perfectly") == ["fit_compat"]
    assert appliance_mentions("It fits perfectly") == []  # no named target: not a checkable need
    assert "dimensions" in appliance_mentions("would not fit on my 4 inch dryer vent")
    assert "electrical" in appliance_mentions("runs on a regular 110v outlet")
    assert "capacity" in appliance_mentions("great for my 5 cup maker")


def test_beauty_detector_uses_pilot_parser():
    assert "skin_type" in beauty_mentions("I have very dry skin and this helped")
    assert beauty_mentions("Shipping was fast") == []
