# Tech Stack

*Stage 4 of [WORKFLOW.md](../WORKFLOW.md). Chosen by full-stack-developer, one entry per module with the reason.*

| Module | Stack | Reason |
|---|---|---|
| Data, parser, benchmark builder, calibrator, evaluator (M1–M6, M9, M12) | Python 3, pandas, NumPy, SciPy (`binom`, `beta`), pytest | Standard-library-first, file-based JSONL so every number reruns from caches; SciPy for exact binomial / Clopper–Pearson |
| LLM matchers, judge, paraphraser (M6–M8) | Claude via the Claude Code CLI (cloud); open-weight models via Ollama (Mac) | The only frontier API reachable from the cloud container; Ollama for open-weight runs and an independent judge; all calls cached by (backend, model, system, prompt) |
| Dense baselines (M7) | PyTorch + transformers (BLaIR, Qwen3-Embedding), rank-bm25 | Hugging Face is reachable from the Mac only |
| Disclosure engine and seller simulator (M10–M11) | Python, same LLM backend | Same caching and opaque-id rules as the matchers |
