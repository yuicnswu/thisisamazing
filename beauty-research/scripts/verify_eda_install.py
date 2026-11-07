"""Exercise the notebook's local tools without making an LLM/API request."""
import base64
import importlib.metadata
import json
from pathlib import Path

import pandas as pd
from ai_data_science_team.ds_agents import EDAToolsAgent
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from ai_data_science_team.tools.eda import (
    describe_dataset,
    visualize_missing,
    generate_correlation_funnel,
    generate_sweetviz_report,
)

root = Path(__file__).resolve().parents[1]
out = root / "output" / "install_smoke"
out.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(root / "vendor/ai-data-science-team/data/churn_data.csv").head(200)
small = df[["Churn", "tenure", "MonthlyCharges", "Contract"]].copy()
small.loc[small.index[:10], "MonthlyCharges"] = float("nan")
results = {"agent_import": EDAToolsAgent.__name__, "sample_rows": len(small)}


class OfflineModel(FakeListChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


try:
    agent = EDAToolsAgent(OfflineModel(responses=["Offline installation check passed."]))
    agent.invoke_agent("Return the installation check message.")
    results["agent_graph_offline"] = {"status": "ok"}
except Exception as exc:
    results["agent_graph_offline"] = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}
for name, tool, kwargs in [
    ("describe_dataset", describe_dataset, {}),
    ("visualize_missing", visualize_missing, {"n_sample": 100}),
    ("generate_correlation_funnel", generate_correlation_funnel,
     {"target": "Churn", "target_bin_index": "Yes"}),
    ("generate_sweetviz_report", generate_sweetviz_report,
     {"target": "Churn", "report_name": "smoke_sweetviz.html", "report_directory": str(out)}),
]:
    try:
        # The funnel requires complete data; missing-data plots intentionally do not.
        tool_data = small.dropna() if name == "generate_correlation_funnel" else small
        content, artifact = tool.func(data_raw=tool_data.to_dict(), **kwargs)
        results[name] = {"status": "ok", "message": content, "artifact_keys": list(artifact)}
        if name == "visualize_missing":
            for key, value in artifact.items():
                (out / f"{key}.png").write_bytes(base64.b64decode(value))
    except Exception as exc:
        results[name] = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}
results["versions"] = {name: importlib.metadata.version(name) for name in [
    "ai-data-science-team", "pandas", "numpy", "langchain", "langgraph", "pytimetk", "sweetviz", "missingno", "jupyterlab"
]}
(out / "verification.json").write_text(json.dumps(results, indent=2, default=str))
print(json.dumps(results, indent=2, default=str))
if any(isinstance(x, dict) and x.get("status") == "failed" for x in results.values()):
    raise SystemExit(1)
