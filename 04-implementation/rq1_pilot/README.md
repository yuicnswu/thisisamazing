# RQ1 pilot: do AI recommenders match on listing evidence or on priors?

Real models on real All_Beauty listings. Replaces the simulated `scripts/run_rq1_rq2_rq3_benchmark.py` for RQ1
(that script hard-codes its outcomes; see `is-topic/neurips-mock-review-v2.md` §1). Results: `05-report/report.md`.

| File | What it does |
|---|---|
| `attributes.py` | §12.1 checkable attributes, rule parser over listing text, `details` normaliser, deterministic support label |
| `data.py` | Loads listings (hackathon cohort + 1,000-item metadata sample). `render()` is all a matcher sees; `details` stays hidden |
| `g0_count.py` | G0 feasibility count (§12.3) |
| `edits.py` | Real edits of real listings: remove, vague, contradict, remove + famous brand + hype, and natural missing evidence |
| `mine_needs.py` | LLM-mined checkable needs from early verified reviews, with automatic checks and a second-model agreement check |
| `matchers.py` | LLM naive prompt, LLM strict "only if stated" prompt, LLM extract-then-rule, keyword rule, dense similarity (BLaIR) |
| `llm.py` | Claude (via the Claude Code CLI) and Ollama backends, cached in `outputs/llm_cache.jsonl` |
| `matchers.nesy_verifier` | Neuro-symbolic verifier: LLM proposes verbatim support / contradiction quotes; a symbolic certificate checks each is verbatim and names the value |
| `conformal.py`, `analyze_conformal.py` | Algorithm 1 of `03-solution-design/theory.md`: fixed-sequence LTT on (λ, τ) for URR and URJ, one item per product, consensus labels |
| `ltt.py` | Learn-then-Test threshold for URR ≤ α on a calibration split, evaluated on held-out products |
| `run_pilot.py`, `analyze.py` | Build items, run matchers, write `outputs/results.{json,md}` |

```bash
pip install pandas pyarrow scipy pytest
python -m pytest -q tests                       # module tests (see 04-implementation/qa.md)
python g0_count.py outputs/g0.json              # needs /mnt/project-files (or PROJECT_FILES=...)
python run_pilot.py build                       # outputs/items.jsonl (already committed)
python run_pilot.py run strict claude claude-sonnet-5-5
python run_pilot.py run naive ollama qwen3:8b   # open-weight, needs a local Ollama
python run_pilot.py run dense hyp1231/blair-roberta-base   # needs torch + transformers + Hugging Face access
python run_pilot.py run keyword
python run_pilot.py run nesy claude claude-sonnet-5-5
POOL=cal LLM_CACHE=outputs/llm_cache_cal.jsonl python run_pilot.py build   # 1,783 more products, one item each
POOL=cal LLM_CACHE=outputs/llm_cache_cal.jsonl python audit_labels.py      # (then `run ...` as above)
python analyze.py
python analyze_conformal.py
```

Matchers see the item only through `Listing.render()` (title, brand, bullets, description). They never see the
`details` field, the variant name or the label. Batches are shuffled across products.
