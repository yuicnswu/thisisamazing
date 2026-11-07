# ABOUTME: Starter volley script: profile Amazon All_Beauty reviews with DuckDB.
# ABOUTME: Copy and renumber for each new volley topic (NN-topic.py matches notebooks/NN-topic.ipynb).
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from eda_query import query, register  # noqa: E402

REVIEWS = os.environ.get("AMAZON_REVIEWS", "~/Downloads/All_Beauty.jsonl")
register("reviews", REVIEWS)

print(query("DESCRIBE reviews", "schema"))
print(query("SELECT COUNT(*) AS n, COUNT(DISTINCT parent_asin) AS products, COUNT(DISTINCT user_id) AS users FROM reviews", "size"))
print(query("SELECT rating, COUNT(*) AS n, ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct FROM reviews GROUP BY 1 ORDER BY 1", "ratings"))
print(query("SELECT YEAR(to_timestamp(timestamp / 1000)) AS yr, COUNT(*) AS n, ROUND(AVG(rating), 2) AS mean_rating FROM reviews GROUP BY 1 ORDER BY 1", "by_year"))
