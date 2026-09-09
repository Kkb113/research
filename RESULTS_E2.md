# E2 results: exact-output fiber preprocessing

This is a production preprocessing-stage result, not a full virtual-unwrapping result. The optional direction loss remains unchanged and off by default. E2 was frozen at `63fe419288d8cc79b1af120a707c2ec3bed2dee5` before this continuation's 31-case execution. Missing E1 source is not claimed reproduced.

## Exactness and baselines

All 112 public source files pass their SHA256 checks. Nine unit tests pass, including 480 scalar-oracle cases with ties, noncontiguous arrays, negative/large origins, ROI boundaries and small tile budgets. On 31 real chunks, four cell sizes, five thresholds and two ROIs, both alternatives exactly match the pinned upstream selector: **2,480 comparisons**. Primary saved selections contain 134,994 records.

Median selection milliseconds across per-case medians of five interleaved calls (c=2, threshold160):

| Volume | Cases | Upstream | Sparse lexsort | Block |
|---|---:|---:|---:|---:|
| PHerc0332 | 8 | 5.478 | 3.976 | 1.638 |
| PHerc1299 | 8 | 3.028 | 2.038 | 1.531 |
| PHerc0139 | 8 | 4.428 | 3.335 | 1.496 |
| PHercParis4 | 7 | 5.569 | 4.269 | 1.650 |

Block beats upstream on 28/31 and sparse sorting on 23/31. Retain regressions; do not infer uniform improvement. Equal-scroll geometric speedup is 2.524x versus upstream and 1.700x versus sparse locally; externally 2.512x and 1.695x. A post-hoc descriptive four-scroll bootstrap gives local conditional intervals [2.093,3.044] and [1.285,2.248]. These condition on sampled chunks/timing medians, have only four clusters and are not universal guarantees or algorithm-selection criteria.

## Actual complete extraction stage

Local-mirror wall seconds include original HTTP listing/reads, decompression, selection, coordinate conversion and output. Each volume has eight sampled real chunks, not its complete source volume. Three timed repetitions follow one warm-up per arm.

| Volume | Upstream | Sparse-only | Block-only | Block+stream | Records |
|---|---:|---:|---:|---:|---:|
| PHerc0332 | 0.2101 | 0.1770 | 0.1283 | 0.1650 | 45,257 |
| PHerc1299 | 0.1704 | 0.1337 | 0.1243 | 0.1197 | 20,928 |
| PHerc0139 | 0.2533 | 0.2176 | 0.2077 | 0.2213 | 30,074 |
| PHercParis4 | 0.2657 | 0.2181 | 0.2039 | 0.2003 | 44,617 |

All four loaded arrays and parsed metadata match within each comparison; the unmodified upstream loader reads the outputs. There were 64 complete extraction calls including warm-ups. Public-network throughput was not measured. Streaming is optional because small jobs may be slower. On an empty fixture work list, the original raises `ValueError: need at least one array to concatenate`; streaming writes a valid zero-sample artifact.

## Output serialization memory

Repeat saved real batches: these are resource workloads, not additional regions. Measure Linux total-process VmHWM before a verifier loads complete output arrays.

| Repetitions | Records | Concatenate MiB | Stream MiB | Concatenate seconds | Stream seconds |
|---|---:|---:|---:|---:|---:|
| 1 | 134,994 | 97.29 | 94.84 | 0.141 | 0.156 |
| 16 | 2,159,904 | 147.73 | 97.10 | 2.393 | 2.381 |
| 128 | 17,279,232 | 386.63 | 97.05 | 19.230 | 18.934 |

Every paired array hash agrees. Raw spool disk at 128x is approximately 247 MiB plus the archive. There is only one measured writer invocation at each size; no significant compression speed gain is claimed. Initial inherited ru_maxrss values were contaminated and are retained only for audit; use `selection_memory_corrected.json`, not the legacy rss_mib fields.

## Clean-machine reproduction completed

[Run 34353180786](https://github.com/Kkb113/research/actions/runs/34353180786) completed successfully from public-source reacquisition and frozen code. All 2,480 configuration records and 155 selection arrays are identical to local results; four extraction-volume output hashes and all six writer-workload/method hash sets match. The external large writer used 330.98 MiB versus 39.09 MiB; 17.010 versus 17.188 seconds confirms the memory benefit is not a claim of universal speed improvement. See EXTERNAL_VALIDATION.md.

Raw per-case outputs and selections are in that run's artifact and the delivered evidence archive. Reproduction does not depend on retaining the temporary artifact. No human timing, expert-baseline win, new winding correctness, repaired switch, readable area, ink or prize is claimed.
