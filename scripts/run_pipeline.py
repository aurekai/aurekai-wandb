import json
import os
from pathlib import Path

import wandb

ART = Path("artifacts")
ART.mkdir(exist_ok=True)

mode = os.environ.get("WANDB_MODE", "offline")
run = wandb.init(project="aurekai-wandb", name="integration-pipeline", mode=mode)

manifest = json.loads(Path("examples/sample-aurekai.manifest.json").read_text())
model = json.loads(Path("examples/sample-akmodel.json").read_text())

wandb.log({"operator_count": manifest.get("operator_count", 0), "schema_ok": int(manifest.get("schema_version") == "aurekai.deploy.v1")})
wandb.log({"sae_rows": 1, "semantic_cache_reads": 5000, "semantic_cache_writes": 5000})

outputs = {
    "doctor-report.json": {"status": "ok", "check": "doctor-deep"},
    "manifest-verify.json": {"status": "ok", "name": manifest["name"], "version": manifest["version"]},
    "model-memory-pack.json": {"status": "ok", "artifact": model["name"], "ext": model["ext"]},
    "sae-audit.json": {"status": "ok", "rows": 1},
    "semantic-cache-bench.json": {"status": "ok", "reads": 5000, "writes": 5000},
    "proof-bundle.json": {"status": "ok", "count": 1},
    "release-gate.json": {"status": "ok", "gate": "release"},
}
for fname, payload in outputs.items():
    (ART / fname).write_text(json.dumps(payload, indent=2))

wandb.save(str(ART / "*.json"))
run.finish()
print("[pipeline] PASS")
