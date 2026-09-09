# Integration: exact-output fiber evidence preprocessing

## Inputs and outputs

Retain the upstream CLI: Lasagna manifest, output NPZ, half-open `--z-roi`, output scale, threshold, cell size and workers. Read `presence`, `nx`, `ny`; retain the upstream scale conversion and coordinate frame. Output format 2 contains `position_zyx` float32 (N,3), `nx`, `ny`, `presence` uint8 (N,), and scalar `metadata_json`.

All selected arrays, ordering and parsed metadata match the original on tested nonempty work. ZIP headers/timestamps need not match. Streaming also emits a valid empty artifact where the original empty-work path raises a concatenate error.

## Installation

Use Python 3.13.5 for the reproduced CPU environment. No GPU is required for this component.

```bash
python -m pip install -e .
python scripts/acquire_e2.py
python -m unittest discover -s tests -v
```

Acquisition decodes the committed manifest parts, verifies the frozen manifest SHA256, then verifies all 112 public inputs and the original upstream module. Hash changes are errors, never silent replacements.

## Minimal selection-only integration

```bash
python -m evidence_pipeline.integrate \
  e2_data/upstream_fiber_direction_samples.py \
  --output fiber_direction_samples_e2.py
```

Run that script with the same arguments as the original. A real, self-contained example is the HTTP-mirror test:

```bash
python scripts/validate_stage.py --fixtures e2_data \
  --upstream e2_data/upstream_fiber_direction_samples.py --out e2_results/stage
```

The patch inserts the exact selector before the extraction entry point. Listing, decoding, coordinate conversion, metadata and loader are unchanged. A different upstream source hash is refused rather than blindly patched.

## Optional streaming output

```bash
python -m evidence_pipeline.integrate \
  e2_data/upstream_fiber_direction_samples.py \
  --stream --output fiber_direction_samples_e2_stream.py
```

This additionally consumes ordered batches with at most twice the worker count pending, spools raw arrays, writes compressed NPY members and atomically publishes an NPZ. Allocate about 15 raw bytes per selected record plus the final compressed file and any existing destination. Disk replaces growing output RAM; small jobs can be slower.

Generate a reviewable patch instead of a complete script:

```bash
python -m evidence_pipeline.integrate \
  e2_data/upstream_fiber_direction_samples.py \
  --stream --diff --output fiber_preprocessing.patch
```

Install this helper package in the upstream script environment, or vendor the small modules with their MIT notices. No model, checkpoint, loss weight, optimizer, geometry metric, ink model or sampling threshold is changed.

## Failure modes and expected benefit

Sparse sorting can outperform block reduction on sparse/empty data. Spool disk can fill. Unsupported dtypes, malformed shapes and source drift fail clearly. The code cannot correct bad predictions or upstream metadata. Selection arrays still require memory and the upstream loader is not out-of-core. Benefit is CPU selection work and output-memory scaling, not reconstruction accuracy.

## Complete reproduction

```bash
bash scripts/reproduce_e2.sh
```

This executes acquisition, oracle/unit tests, all fixed-corpus comparisons, full extraction-stage tests and corrected memory/resource tests. See RESULTS_E2.md and LIMITATIONS.md before interpreting any number.
