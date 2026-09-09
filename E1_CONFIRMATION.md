# E1 confirmation freeze — 9 September 2026

This supplements ENGINEERING_PROTOCOL.md, committed at 2bb3d92d51253a8a9008ee588e82a5ff78820db4. No confirmation chunk has been evaluated for algorithm performance or correctness before this freeze. Metadata and source-byte acquisition were inspected; development used ONLY PHercParis4_86.44.42 and declared synthetic cases.

## Development decision
The offset-loop reducer beat the upstream implementation, but a simpler reshape/argmax comparator was better at c=2,4,8 on the development chunk. Ship the simpler tiled reduction, not the more elaborate method. At c=1 use direct threshold coordinates; at c>32 use threshold-first sparse sorting. These are known reductions and engineering decisions, not new mathematics. Retain every comparator and the c=8 offset-loop regression. No scroll-specific or density-tuned dispatch.

The initial writer implementation failed two zero-length-batch tests because memoryview.cast rejects zero-shaped arrays. It was fixed before confirmation by skipping zero-sized writes; the issue is retained in the development log. A separate codec bootstrap workflow first failed YAML parsing and was corrected; that was setup failure, not a scientific result.

## Frozen files (SHA-256)
- evidence_pipeline/select.py: 5c4fd54df0dc19e56c4b948f72e16b0c0b737f805d7f25259e4abc4e2e78ce28
- evidence_pipeline/stream.py: 9929e9dcdc253614d295b8ad0574b9ea4ff78d13e36c10b4179f8f638acf9228
- evidence_pipeline/extractor.py: 5c97333aa0c69df60dae06c005d046776c5ad4ac1f3f4aefb0a2366d59eefc66
- evidence_pipeline/fixtures.py: 51b29f88a6f1c5410aaa16a1ad1f018dfd16bfd1ec98db49d3c7ca3679fcb899
- scripts/confirm_selection.py: 5803435453becf8331aacd5523ee3d0363017fe6179a0432cda741fa136d3431
- provenance/fiber_manifest.json: b4683eb73b8b5756935696c1382edcfba42bb813ab4d0ad56f983aa63ad8bb9f

Full source is retained locally and will be published with the results; these hashes prevent silently revising it after confirmation. The manifest pins 32 original chunk triplets across four volumes; the first Paris4 case is development, the other 31 are confirmation. Public acquisition completed with no exclusions or sampling-frame change. Full presence listings contained 16,864 / 24,226 / 113,437 / 166,032 stored chunks for 0332 / 1299 / 0139 / Paris4 respectively. This inventory is not a count of correct fibers.

## Confirmation execution details
All 31 confirmation cases: c in {1,2,4,8}, thresholds {0,80,160,240,255}, full and clipped ROI; four alternatives compared exactly to upstream. Save primary selected coordinates, flat indices and direction/confidence bytes. Independent scalar-oracle tests already cover arbitrary alignment, negative/large origins, boundaries, ties, empty arrays and noncontiguous layout; 47 unit cases currently pass.

Timing: production-default c=2 and threshold160 on all31; also c=8 on the first confirmation case in each scroll (chosen by existing manifest order). Compare upstream, threshold-first sparse sorting, offset loops, and the chosen simple tiled method. One isolated resident subprocess per case/method, one warm-up, then five interleaved timed calls, method order shuffled using seed20260909. The parent requests one timed call at a time, so timing workers do not compete. Fixed BLAS/OpenMP thread count1. Report total process RSS, not only an inflated percentage of incremental allocations. Record per-case digests, counts, timing and RSS. Repeated timing calls are not independent scroll evidence.

Dependencies for CPU component validation: Python3.13, NumPy2.3.5, numcodecs0.16.5, requests2.32.5. This is the exact upstream CPU extraction module, not a claim to satisfy the complete current GPU fitter environment (which declares Python>=3.14 and newer package minima).

## Full-stage integration experiment planned before results
Use a local HTTP mirror with the same immutable compressed real chunks. Preserve original shape, scale and coordinates; serve S3-shaped listing responses for only the declared fixture keys. A test-only DNS mapping sends a synthetic S3 hostname to localhost; no extraction algorithm or listing function is substituted. This fixture contains a sparse subset of the volume, not all stored public chunks. Compare original extraction, sparse-selection-only, tiled-selection-only, and complete bounded writer integration with identical input requests, worker count1, ROI and output. Compare all four output arrays and parsed format2 metadata; archive timestamps/ZIP headers need not be identical. Execute upstream loader on outputs. Full-stage times include HTTP loopback, decoding, selection and compression, not real public-network download speed. Five repetitions per volume; fixed interleaved order seed20260909. Preserve a warm-up per arm.

Serialization stress uses repeated batches from these real selections, explicitly labeled a resource workload, not additional real regions. Compare 1x,16x,128x repeats of the complete primary confirmation output; exact arrays must match. Report spool-disk requirements and compression time even if slower. Run each writer in a fresh process; do not infer reconstruction accuracy from this experiment.

No new labels, expert time study, GPU optimization, improved ink, or prize acceptance is claimed by this protocol.
