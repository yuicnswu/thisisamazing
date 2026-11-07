# ABOUTME: Read-only SQL helper for EDA volleying: DuckDB over local files, or a Databricks SQL warehouse.
# ABOUTME: Workflow adapted from carteakey/claude-databricks-eda; this code is written fresh for this repo.
"""Run read-only SQL during an EDA volley and get a pandas DataFrame back.

Local backend (default): DuckDB queries CSV, JSONL and Parquet files in place, so
the Amazon All_Beauty and Sephora downloads need no loading step.

    from eda_query import query
    df = query("SELECT rating, COUNT(*) AS n FROM read_json_auto('~/Downloads/All_Beauty.jsonl') GROUP BY 1")

Register short table names once per session with ``register``:

    register("reviews", "~/Downloads/All_Beauty.jsonl")
    query("SELECT AVG(rating) FROM reviews")

Databricks backend (optional): set EDA_BACKEND=databricks and
DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, DATABRICKS_ACCESS_TOKEN in the
environment or in a .env file that is never committed. TLS verification stays on.
"""
from __future__ import annotations

import os
import re
import time
from pathlib import Path

import pandas as pd

_ALLOWED_START = re.compile(r"^\s*(SELECT|WITH|DESCRIBE|DESC|SHOW|SUMMARIZE|EXPLAIN|FROM)\b", re.I)
_BLOCKED = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|CREATE|ALTER|TRUNCATE|GRANT|REVOKE|COPY|ATTACH|DETACH|INSTALL|LOAD|EXPORT|IMPORT|SET|PRAGMA|CALL|VACUUM|OPTIMIZE)\b",
    re.I,
)
_STRINGS_AND_COMMENTS = re.compile(r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"|--[^\n]*|/\*.*?\*/", re.S)

_con = None


def check_read_only(sql: str) -> None:
    """Raise ValueError unless ``sql`` is a single read-only statement."""
    bare = _STRINGS_AND_COMMENTS.sub("''", sql).strip().rstrip(";")
    if ";" in bare:
        raise ValueError("Only one statement per query.")
    if not _ALLOWED_START.match(bare):
        raise ValueError("Only SELECT, WITH, FROM, DESCRIBE, SHOW, SUMMARIZE and EXPLAIN are allowed.")
    hit = _BLOCKED.search(bare)
    if hit:
        raise ValueError(f"Blocked keyword in query: {hit.group(1).upper()}")


def _duckdb():
    global _con
    if _con is None:
        import duckdb

        _con = duckdb.connect()
    return _con


def register(name: str, path: str | os.PathLike) -> None:
    """Expose a CSV, JSONL/JSON or Parquet file as view ``name`` (local backend only)."""
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ValueError(f"Bad view name: {name!r}")
    p = Path(path).expanduser()
    suffixes = "".join(p.suffixes).lower()
    if ".parquet" in suffixes:
        reader = "read_parquet"
    elif ".json" in suffixes:
        reader = "read_json_auto"
    elif ".csv" in suffixes or ".tsv" in suffixes:
        reader = "read_csv_auto"
    else:
        raise ValueError(f"Unknown file type: {p}")
    literal = str(p).replace("'", "''")
    _duckdb().execute(f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM {reader}('{literal}')")


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    for d in (Path.cwd(), *Path.cwd().parents):
        if (d / ".env").exists():
            load_dotenv(d / ".env")
            return


def _databricks(sql: str, timeout: int) -> pd.DataFrame:
    import requests

    _load_env()
    host = os.environ.get("DATABRICKS_SERVER_HOSTNAME", "").removeprefix("https://").strip("/")
    http_path = os.environ.get("DATABRICKS_HTTP_PATH", "")
    token = os.environ.get("DATABRICKS_ACCESS_TOKEN", "")
    if not (host and http_path and token):
        raise ValueError("Set DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH and DATABRICKS_ACCESS_TOKEN.")
    headers = {"Authorization": f"Bearer {token}"}
    base = f"https://{host}/api/2.0/sql/statements"
    body = {
        "statement": sql,
        "warehouse_id": http_path.rstrip("/").split("/")[-1],
        "wait_timeout": "30s",
        "on_wait_timeout": "CONTINUE",
        "format": "JSON_ARRAY",
        "disposition": "INLINE",
    }
    r = requests.post(base, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    res = r.json()
    deadline = time.monotonic() + timeout
    while res["status"]["state"] in ("PENDING", "RUNNING"):
        if time.monotonic() > deadline:
            requests.post(f"{base}/{res['statement_id']}/cancel", headers=headers, timeout=30)
            raise TimeoutError(f"Query exceeded {timeout}s")
        time.sleep(2)
        r = requests.get(f"{base}/{res['statement_id']}", headers=headers, timeout=60)
        r.raise_for_status()
        res = r.json()
    if res["status"]["state"] != "SUCCEEDED":
        raise RuntimeError(res["status"].get("error", res["status"]))
    cols = [c["name"] for c in res["manifest"]["schema"]["columns"]]
    rows = list(res.get("result", {}).get("data_array", []) or [])
    chunk = res.get("result", {}).get("next_chunk_internal_link")
    while chunk:
        r = requests.get(f"https://{host}{chunk}", headers=headers, timeout=60)
        r.raise_for_status()
        part = r.json()
        rows += part.get("data_array", []) or []
        chunk = part.get("next_chunk_internal_link")
    return pd.DataFrame(rows, columns=cols)


def query(sql: str, name: str | None = None, timeout: int = 300, show: bool = True) -> pd.DataFrame:
    """Run one read-only statement and return a DataFrame. Prints shape and timing if ``show``."""
    check_read_only(sql)
    backend = os.environ.get("EDA_BACKEND", "duckdb").lower()
    t0 = time.monotonic()
    if backend == "databricks":
        df = _databricks(sql, timeout)
    elif backend == "duckdb":
        df = _duckdb().execute(sql).df()
    else:
        raise ValueError(f"Unknown EDA_BACKEND: {backend}")
    if show:
        print(f"[{name or 'query'}] {df.shape[0]:,} rows x {df.shape[1]} cols in {time.monotonic() - t0:.1f}s ({backend})")
    return df
