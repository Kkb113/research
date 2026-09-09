# E2: resumed exact-output fiber preprocessing validation

Date: 2026-09-09. Scope: CPU preprocessing inside the actual pinned Vesuvius fiber-direction extractor, not the GPU optimizer, reconstructed geometry, ink recovery, or human annotation efficiency.

## Continuation and provenance
E1_CONFIRMATION.md described locally retained source whose bytes/results were not available in the current runtime or published in this repository. E2 is a new implementation; it must not be described as reproducing the missing E1 source hashes. The original E1 protocols remain unchanged. We recovered the original 32 chunk triplets from four public volumes and verified all 112 manifest-recorded source files after restoring the originally omitted hidden metadata. The source volumes are PHerc0332, PHerc1299, PHerc0139, PHercParis4. E1's hash-based input sampling is unchanged. As prior-session inspection cannot be independently established, report this as fixed-corpus validation, not a newly independent or untouched scientific efficacy replication.

Upstream: ScrollPrize/villa 4accc199a55695ebbefaab4fb6a99faa800fcabf, spiral-fitting/fiber_direction_samples.py. Data manifest SHA256: b4683eb73b8b5756935696c1382edcfba42bb813ab4d0ad56f983aa63ad8bb9f.

Development in this continuation used only synthetic cases and PHercParis4_86.44.42. No other corpus chunk has been evaluated in this continuation before this commit. Nine tests currently pass, including a test exercising 480 independent scalar-oracle cases. Development is not a confirmation result.

## Frozen implementation
- evidence_pipeline/select.py SHA256 64f0523ec1d01eded50904ab62bdfa892c1d8c2f5e8528e71b7f40c0db05f60d
- evidence_pipeline/stream.py SHA256 84e842ccc6758517a06bbbad60885ba8b0fc6e7b0f594c98b7b9754fb07091fc
- evidence_pipeline/fixtures.py SHA256 380e2dbe29606ac4a2c016467951af50779f3ee03f4f54f78c17bd049f206541

Select maximum uint8 presence per GLOBAL cell, restrict to the same half-open ROI, break ties by original C-order flat index, and emit cells lexicographically. The implementation uses ordinary block/argmax reduction. c=1 is direct threshold selection; c>32 or cells larger than the tile budget use threshold-first sparse sorting. No density/scroll-specific dispatch or hyperparameter tuning after this freeze. Tile budget 1048576 voxels. Output memory is unavoidable and NOT claimed bounded by this tile budget.

## Correctness and performance
Use all remaining 31 fixed corpus cases. Compare pinned upstream, threshold-first sparse lexsort, and chosen block reduction. Correctness grid: c={1,2,4,8}, thresholds={0,80,160,240,255}, full ROI and clipped ROI (offset [1,3,5], end offset [2,4,6]). Exact indices, coordinates, direction bytes, presence bytes and ordering are required. Save primary outputs and SHA256 digests. No test-case exclusions for foreground fraction or speed.

Primary timing: c=2, threshold160, full ROI. One warm-up per method and five interleaved calls in seeded random order (seed20260909). One active timing call at a time, OpenMP/BLAS thread count1. Separately run each method/case in a fresh subprocess for total process peak RSS. Report absolute seconds and MiB, per-volume medians, per-case ratios, and regressions. Repetitions are not independent scrolls. Timing intervals, if shown, condition on these source chunks and environment.

## Full-stage integration
Patch the actual extractor's selection function; a separate complete arm also replaces retained output batches/concatenation with ordered bounded producer consumption and streaming NPZ serialization. Original decoding, scale conversion, selection policy, loader, coordinate system, thresholds and metadata definitions remain frozen. Compare original, sparse-only, block-only, and block+stream arms on a local HTTP mirror of the 32 immutable real chunk triplets (8 per volume), with truthful S3-shaped listings restricted to these fixtures. No synthetic fiber volume and no geometry correction is substituted. Report local-mirror stage wall time (HTTP, decoding, selection, writing) explicitly, not public-network performance or full-scroll time. Three interleaved repetitions and one warm-up per arm/volume. All four loaded arrays and parsed metadata must match, and upstream's loader must read them. Include zero-work and publication-failure tests.

Serialization resource experiment: replay the saved real batches 1x,16x,128x; this is repeated-data load testing, not new evidence. Compare original concatenate/save versus spool/write. Run fresh subprocesses; report disk tradeoff and compression time, including slower results. No invented human-time or GPU measurements.

## Acceptance and reporting
Publish code, patch, tests, original inputs or hash-verified reacquisition, per-case timings, errors, environment and failed results. Require exact output equality, practical resource improvement, and a small documented integration surface. External-machine execution is computational reproduction only. No reconstruction improvement, expert superiority, calibrated annotation cost, independent biological ground truth, prize, or methodological novelty is claimed. If external execution is blocked, explicitly mark it uncompleted rather than infer success.
