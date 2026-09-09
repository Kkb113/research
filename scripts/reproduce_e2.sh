#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python -m pip install -e .
python scripts/acquire_e2.py
mkdir -p e2_results
python -m unittest discover -s tests -v 2>&1 | tee e2_results/tests.txt
python scripts/validate_selection.py --fixtures e2_data --upstream e2_data/upstream_fiber_direction_samples.py --out e2_results | tee e2_results/selection.log
python scripts/validate_stage.py --fixtures e2_data --upstream e2_data/upstream_fiber_direction_samples.py --out e2_results/stage | tee e2_results/stage.log
python scripts/validate_resources.py --fixtures e2_data --upstream e2_data/upstream_fiber_direction_samples.py --results e2_results | tee e2_results/resources.log
python -m pip freeze > e2_results/environment.txt
