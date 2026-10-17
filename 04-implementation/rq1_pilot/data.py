"""Load real All_Beauty listings: visible text (title, bullets, description) and the hidden `details` field."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

import pandas as pd

PROJECT = os.environ.get("PROJECT_FILES", "/mnt/project-files")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COHORT_CSV = os.path.join(PROJECT, "data", "hackathon_beauty_gmv.csv")
META_SAMPLE_CSV = os.path.join(REPO, "meta_All_Beauty_sample_1000.csv")
REVIEWS_JSONL = os.path.join(PROJECT, "All_Beauty.jsonl")


@dataclass
class Listing:
    asin: str
    title: str
    bullets: list[str]
    description: list[str]
    details: dict
    store: str = ""
    source: str = ""
    meta: dict = field(default_factory=dict)

    def visible_text(self) -> str:
        parts = [self.title] + self.bullets + self.description
        return "\n".join(p for p in parts if p)

    def render(self) -> str:
        """What a matcher sees. `details` is never shown (plan §11.1)."""
        lines = [f"Title: {self.title}"]
        if self.store:
            lines.append(f"Brand: {self.store}")
        if self.bullets:
            lines.append("About this item:")
            lines += [f"- {b}" for b in self.bullets]
        if self.description:
            lines.append("Description: " + " ".join(self.description))
        return "\n".join(lines)


def _s(x) -> str:
    return "" if x is None or (isinstance(x, float) and pd.isna(x)) else str(x)


def _jlist(x) -> list[str]:
    x = _s(x)
    if not x:
        return []
    try:
        v = json.loads(x)
        return [str(i) for i in v] if isinstance(v, list) else [str(v)]
    except json.JSONDecodeError:
        return [x]


def load_listings() -> list[Listing]:
    """Unique listings from the hackathon cohort plus the 1,000-item metadata sample, deduped by parent_asin."""
    out: dict[str, Listing] = {}
    if os.path.exists(COHORT_CSV):
        cols = ["parent_asin", "product_title", "features_text", "description_text", "details_json", "store_brand",
                "meta_rating_number", "meta_average_rating"]
        df = pd.read_csv(COHORT_CSV, usecols=cols).drop_duplicates("parent_asin")
        for r in df.itertuples(index=False):
            feats = [b.strip() for b in _s(r.features_text).split(" | ") if b.strip()]
            desc = [_s(r.description_text)] if _s(r.description_text) else []
            det = json.loads(r.details_json) if _s(r.details_json) else {}
            out[r.parent_asin] = Listing(r.parent_asin, _s(r.product_title), feats, desc, det, _s(r.store_brand), "cohort",
                                         {"rating_number": r.meta_rating_number, "average_rating": r.meta_average_rating})
    if os.path.exists(META_SAMPLE_CSV):
        df = pd.read_csv(META_SAMPLE_CSV)
        for r in df.itertuples(index=False):
            if r.parent_asin in out:
                continue
            det = json.loads(r.details) if _s(r.details) else {}
            out[r.parent_asin] = Listing(r.parent_asin, _s(r.title), _jlist(r.features), _jlist(r.description), det,
                                         _s(r.store), "meta_sample",
                                         {"rating_number": r.rating_number, "average_rating": r.average_rating})
    return list(out.values())
