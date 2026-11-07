#!/usr/bin/env bash
# Full text-analysis pipeline for one source, in order. Usage: bash run_full.sh sephora [path-to-raw-data]
# Steps needing Claude models use the Claude CLI (CLAUDE_BIN if it is not on PATH).
# scale_embed.py needs: pip install sentence-transformers (and Hugging Face access).
set -euo pipefail
cd "$(dirname "$0")"
S=$1
[ -f "outputs/$S/reviews.parquet" ] || python parse.py "$S" "$2"
[ -f "outputs/$S/topics.json" ] || python discover.py "$S"
python rq3_temporal.py "$S" 2>&1 | tee "outputs/$S/rq3.log" || true     # Sephora only; needs no labels
python codebook.py "$S" --workers 8 2>&1 | tee "outputs/$S/codebook.log"   # self-refining guide + jury gold labels
python entail.py "$S" --workers 8 2>&1 | tee "outputs/$S/entail.log"       # semantic support check of gold labels
python topicgpt.py "$S" --workers 8 2>&1 | tee "outputs/$S/topicgpt.log"   # taxonomy coverage audit
python scale.py "$S" 2>&1 | tee "outputs/$S/scale.log"
python analyze.py "$S" > "outputs/$S/analyze.log"
if python -c "import sentence_transformers" 2>/dev/null; then
  python scale_embed.py "$S" 2>&1 | tee "outputs/$S/scale_embed.log"
  PREDICTIONS=predictions_emb.parquet python analyze.py "$S" > "outputs/$S/analyze_emb.log"
fi
