#!/usr/bin/env bash
set -euo pipefail
WANDB_MODE=offline python3 scripts/run_pipeline.py >/dev/null
echo "[doctor-deep] PASS"
