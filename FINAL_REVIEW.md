# Final E2 technical review — 9 September 2026

## Completed, narrowly scoped contribution

The delivered component accelerates exact fiber-evidence selection in the pinned Vesuvius CPU extractor and optionally writes its output without concatenating all batches in RAM. This is not a new reconstruction method, proof of improved annotation efficiency, recovered ink, or a prize claim. The optional direction loss is still off by default; no maintainer adoption has been established.

## Completed executions

Original clean-machine validation: https://github.com/Kkb113/research/actions/runs/34353180786

Final review/reproduction: https://github.com/Kkb113/research/actions/runs/34356938694

Final executed commit: `25af9a6a450049264b078c4cd6c2eb553aeb893f`.
Final artifact: `10106283376` (`e2-final-review`), SHA256 `fbf769ea72c738f7d9b433c1886739d72253ba1dc09569c82995b373bacb087b`.
Upstream commit: `4accc199a55695ebbefaab4fb6a99faa800fcabf`.
The E2 selector, streaming writer and fixture-loader bytes remain identical to their protocol hashes. No algorithm was changed during final review.

## Direct artifact checks

The two downloaded executions have 2,480 identical configuration records, 155 identical saved selection arrays, identical four-volume output hashes/counts, and identical writer-output hashes at all three workload sizes. Within each execution every candidate stage output was compared by array shape, dtype and values with the original output: 96 direct array comparisons across the two executions. Parsed metadata is equal within each run; cross-run comparison removes only the loopback manifest URL because server ports differ. The audit is executable as `python scripts/audit_e2_artifacts.py ORIGINAL_RESULTS REPEAT_RESULTS --out audit.json`.

All 112 reacquired public input files passed local SHA256 rechecking after downloading the final artifact. The source package built and installed locally without source changes; its installed console entry point ran outside the source directory and generated both selection-only and optional streaming patches.

## Adversarial tests added after confirmation

13 test methods pass locally and externally. The original nine include 480 scalar-oracle cases. Four added review tests cover all 6,561 2x2x2 arrays on {0,1,255} under three fixed cell/ROI/threshold configurations and two selectors (39,366 comparisons), a competing-writer no-clobber race, serialization failure preserving an existing destination, and noncontiguous output batches. These are post-confirmation software tests, not independent real-scroll observations.

## Reproduction sensitivity, not best-run selection

| Measurement | Original external run | Final repeat |
|---|---:|---:|
| Equal-scroll geometric selection speedup vs upstream | 2.512x | 3.407x |
| Same measure vs sparse-sort control | 1.695x | 1.672x |
| Faster than upstream, primary cases | 28/31 | 29/31 |
| Faster than sparse-sort control | 23/31 | 22/31 |
| Largest writer concatenate peak RSS | 330.98 MiB | 330.74 MiB |
| Largest writer streaming peak RSS | 39.09 MiB | 40.72 MiB |
| Largest writer concatenate time | 17.010 s | 19.613 s |
| Largest writer streaming time | 17.188 s | 19.793 s |

The writer workload repeats real selections to 17,279,232 records; it is not additional regions. Streaming saves about 88% of measured peak process memory here but is slightly slower. It needs approximately 247 MiB raw spool disk plus the final archive. Timing varies across execution environments. No universal speedup or reconstruction-memory bound is claimed.

Complete local-mirror extraction time (original / block-only), seconds:

| Volume | Original external | Final repeat |
|---|---|---|
| PHerc0332 | 0.1968 / 0.1220 | 0.2539 / 0.1619 |
| PHerc1299 | 0.1304 / 0.1126 | 0.2021 / 0.1555 |
| PHerc0139 | 0.2183 / 0.1950 | 0.3130 / 0.2582 |
| PHercParis4 | 0.2205 / 0.1905 | 0.2938 / 0.2477 |

Each mirror has eight immutable chunk triplets, not a full volume. These are actual extraction entry-point measurements, including HTTP loopback, decode, coordinate conversion, selection and writing, not public-network measurements.

## Retained failures and unfinished gates

The original E1 source was not recovered; E2 is explicitly a new implementation. Earlier setup failures and the invalidated inherited ru_maxrss values remain recorded. Sparse/empty regressions are retained. An optional third local timing replay during final review hit the command timeout after nine completed cases; no partial statistics from it are used. Both complete external runs succeeded. Local software/oracle tests and package checks completed.

No GPU optimizer, expert selection comparison, qualified human timing, sheet-switch reduction, recovered readable area or downstream ink improvement was executed. Runpod skills were connected but no callable control-plane tool or configured CLI credential was available in this conversation. No independent AI agents were used.

Technical feedback was requested in https://github.com/ScrollPrize/villa/issues/1746 . At final inspection it was open with no replies. That is a review request, not acceptance. The largest scientific priority remains trustworthy constraint generation/incorporation under real effort budgets; this smaller exact-output engineering contribution is ready for technical inspection.
