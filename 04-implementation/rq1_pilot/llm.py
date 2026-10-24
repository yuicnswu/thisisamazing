"""LLM backends with an on-disk cache.

* `claude`: Claude models through the Claude Code CLI (`claude -p`), the only frontier API reachable from
  the cloud environment this pilot ran in. No tools, a fixed system prompt, no session persistence.
* `ollama`: any open-weight model served by a local Ollama (`OLLAMA_HOST`, default http://localhost:11434).

Every call is cached by (backend, model, system, prompt) so reruns are free and results are reproducible.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import threading
import urllib.request

CACHE = os.environ.get("LLM_CACHE", os.path.join(os.path.dirname(__file__), "outputs", "llm_cache.jsonl"))
_lock = threading.Lock()
_mem: dict[str, str] | None = None


def _key(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()


def _load():
    global _mem
    if _mem is None:
        _mem = {}
        if os.path.exists(CACHE):
            with open(CACHE) as f:
                for line in f:
                    try:
                        r = json.loads(line)
                        _mem[r["k"]] = r["v"]
                    except (json.JSONDecodeError, KeyError):
                        continue
    return _mem


def _claude(model: str, system: str, prompt: str, timeout: int = 600) -> str:
    cmd = ["claude", "-p", "--model", model, "--system-prompt", system, "--tools", "", "--no-session-persistence",
           "--setting-sources", "", "--output-format", "json"]
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, cwd="/tmp")
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-500:] or p.stdout[-500:])
    d = json.loads(p.stdout)
    if d.get("is_error"):
        raise RuntimeError(str(d.get("result"))[:500])
    return d["result"]


def _ollama(model: str, system: str, prompt: str, timeout: int = 900) -> str:
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    if not host.startswith("http"):
        host = "http://" + host
    body = json.dumps({"model": model, "stream": False, "think": False, "options": {"temperature": 0, "num_ctx": 16384},
                       "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]})
    req = urllib.request.Request(host + "/api/chat", body.encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())["message"]["content"]


def complete(backend: str, model: str, system: str, prompt: str, retries: int = 3) -> str:
    k = _key(backend, model, system, prompt)
    mem = _load()
    if k in mem:
        return mem[k]
    fn = {"claude": _claude, "ollama": _ollama}[backend]
    err = None
    for _ in range(retries):
        try:
            out = fn(model, system, prompt)
            break
        except Exception as e:  # noqa: BLE001 - retried, then surfaced
            err = e
    else:
        raise RuntimeError(f"{backend}:{model} failed: {err}")
    with _lock:
        mem[k] = out
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "a") as f:
            f.write(json.dumps({"k": k, "backend": backend, "model": model, "v": out}) + "\n")
    return out


def parse_json(text: str):
    """First JSON array or object in a model reply (models sometimes wrap it in prose or fences)."""
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1)
    for opener, closer in (("[", "]"), ("{", "}")):
        i, j = text.find(opener), text.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(text[i:j + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError("no JSON in reply: " + text[:200])
