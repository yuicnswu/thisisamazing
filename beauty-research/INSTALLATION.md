# Reproduce the Beauty research analyses

Use Python 3.12 from this directory (`beauty-research/`):

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-eda.lock.txt
.venv/bin/python -m ipykernel install --sys-prefix --name beauty-eda --display-name "Beauty EDA (Python 3.12)"
```

Download the original datasets under their respective terms. Defaults are `~/Downloads/meta_All_Beauty.jsonl`, `~/Downloads/All_Beauty.jsonl`, and the six Sephora CSVs in `~/Downloads/archive/`. Override Amazon inputs with `--input` and `--reviews`; override the Sephora directory with `SEPHORA_SOURCE_DIR`.

```sh
.venv/bin/python scripts/beauty_eda.py
.venv/bin/python scripts/add_beauty_reviews.py
.venv/bin/python scripts/beauty_research_workflow.py
.venv/bin/python scripts/add_sephora.py
.venv/bin/python -m jupyterlab notebooks
```

The dependency lock pins the EDA tools source revision. The optional upstream example and installation smoke-check require the vendor checkout:

```sh
git clone https://github.com/business-science/ai-data-science-team.git vendor/ai-data-science-team
git -C vendor/ai-data-science-team checkout 4ffeb7f38178aa250917f29b01355f8b89ba809e
```

Published notebooks have cleared outputs. Runners generate full local HTML and Parquet outputs; source registries and aggregate reports are included in GitHub. Skills guide the authored analysis; installing them is not required to execute the deterministic scripts. No LLM API is called by the integration workflows. The upstream LLM example requires separately configured credentials.

Original source hashes and source-record ordinals support auditability. Row-level review datasets, reviewer identifiers and raw downloads are deliberately excluded from this publication package. Local paths in published manifests use portable placeholders. Existing verification files describe the original local runs; code in this publication package additionally has portable source defaults. Temporal eligibility is not a frozen benchmark, and no model experiment has been run.
