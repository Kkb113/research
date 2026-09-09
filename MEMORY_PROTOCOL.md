# Bounded-memory influence evaluation: prospective protocol

Status: candidate engineering experiment; no production unwrapping or annotation-time benefit is claimed.

Upstream target: ScrollPrize/villa commit 4accc199a55695ebbefaab4fb6a99faa800fcabf, spiral-fitting/influence.py, influence_weight.

Question: Can two-axis tiling preserve the current finite-input influence weights while imposing a strict upper bound on each pairwise temporary array? The bound is not a total GPU allocator-memory guarantee. A latency improvement is not assumed.

Before confirmation, preserve the original upstream function and hash. Compare it directly to the replacement. Fix finite positive limits and sigma; exercise empty inputs, periodic seams, hard-cutoff boundaries, duplicated points, query permutations, float32/float64 source inputs, and footprint sizes exceeding the pair budget. Confirm selected tensor devices and document CUDA availability.

Use seeds 20260909 through 20260918. Compare identical inputs, dtypes, threads, and warmup schedules. Include both large default tiles and small adversarial budgets. Record every case, maximum absolute output error, equality, runtime, and derived maximum pairwise tile size. Timings are kernel timings, not end-to-end fitter measurements. Do not call input points transformed by an approximate coordinate map production spiral-space inputs.

Primary correctness gate: finite-input outputs agree with direct upstream evaluation within float32 tolerance (atol 2e-6, rtol 2e-6), with exact cutoff classification checked separately. Strict mathematical gate: every pairwise tensor has at most chunk_elements entries. No speedup criterion is preregistered; slower cases must remain in the record.

Public annotation/mesh fixtures may be used to exercise sizes and input distributions, but without actual checkpoint-transformed coordinates they are real-data-derived microbenchmarks only. GPU and full-fitter integration remain separate gates. Any change after examining confirmation output requires a new protocol and disjoint confirmation inputs.
