---
name: eda-volley
description: Iterative "volley" EDA on the beauty review data (Amazon All_Beauty, Sephora) with read-only SQL, ending in a documented notebook when the user says "punch it". Use when the user says "volley", "let's volley on", "punch it", or asks for exploratory analysis of a dataset in this repo.
---

# EDA volleying

Adapted from the workflow in [carteakey/claude-databricks-eda](https://github.com/carteakey/claude-databricks-eda). Queries run on local files through DuckDB by default; a Databricks SQL warehouse is an optional backend.

## The loop

1. **The user asks**: "Let's volley on <dataset> to understand <question>."
2. **You write** a script in `beauty-research/notebooks/temp_code/NN-<topic>.py`. `NN` is the two-digit prefix of the notebook it will become. Start from `01-initial_dataset_exploration.py`.
3. **You run it** from that folder, look at the output, and reply with the numbers, what they mean, and any gap between what we expected and what came back (missing values, odd distributions, duplicates, joins that drop rows). Say what you would check next.
4. **Repeat** until the user says **"punch it"**.
5. **On "punch it"**: reread the volley and every `NN-*.py` for that prefix, then write or update `beauty-research/notebooks/NN-<topic>.ipynb`: code cells in the order the analysis built up, each followed by a markdown cell giving the finding and the reasoning. Then run the QA step below and report back.
6. The user runs the notebook to confirm. That ends the cycle.

## Querying

Use `beauty-research/scripts/eda_query.py`. It accepts only one read-only statement per call (SELECT, WITH, FROM, DESCRIBE, SHOW, SUMMARIZE, EXPLAIN) and returns a pandas DataFrame.

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))  # in notebooks: Path.cwd().parent / "scripts"
from eda_query import query, register

register("reviews", "~/Downloads/All_Beauty.jsonl")        # also .csv, .parquet
register("meta", "~/Downloads/meta_All_Beauty.jsonl")
df = query("SELECT rating, COUNT(*) AS n FROM reviews GROUP BY 1 ORDER BY 1", "ratings")
```

- Default data locations follow `beauty-research/INSTALLATION.md`: Amazon files in `~/Downloads/`, Sephora CSVs in `~/Downloads/archive/` (override with `SEPHORA_SOURCE_DIR`). Take paths from environment variables in scripts, never hard-code a personal path.
- Aggregate in SQL. Pull row-level samples only with `LIMIT`.
- Databricks: set `EDA_BACKEND=databricks` and `DATABRICKS_SERVER_HOSTNAME`, `DATABRICKS_HTTP_PATH`, `DATABRICKS_ACCESS_TOKEN` in a `.env` that is gitignored. Ask the user before using it; do not ask for a token in chat.

## Quality check before handing back a notebook

- `pip install -r beauty-research/requirements-volley.txt` if `duckdb` or `jupytext` is missing.
- `jupytext --to py:percent NN-<topic>.ipynb -o /tmp/check.py` and run it from `beauty-research/notebooks/`. Fix every error.
- The notebook imports with `Path.cwd().parent / "scripts"`, never `__file__`: `grep -n "__file__" beauty-research/notebooks/NN-<topic>.ipynb` must print nothing.
- Look for duplicate import cells and code that landed in markdown cells after conversion.
- Cast numeric columns with `pd.to_numeric` when a backend returns strings (Databricks does).
- Clear outputs before committing (`jupyter nbconvert --clear-output --inplace`). Published notebooks in this repo have cleared outputs.

## Project rules that apply

- Follow `WORKFLOW.md`. EDA findings feed the literature review and solution design; when a volley changes a number already reported (for example in `EDA.md`, `beauty-research/README.md` or a proposal), update that document in the same change and say so.
- Never commit raw downloads, row-level review data or reviewer identifiers. Commit scripts, notebooks with cleared outputs, and aggregate tables only.
- Report what the data shows. Label anything not computed from the data as a hypothesis.
- Every script starts with two `# ABOUTME:` comment lines saying what it does.
