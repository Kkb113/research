# Protocol E1: exact sparse-evidence extraction

Committed 2026-09-09 before implementing or benchmarking the new algorithms. Existing annotation-selection replay remains archived evidence, not production validation.

## Decision and scope
Current official open problems identify reliable sparse winding/fiber evidence and data-scale infrastructure as needs. Prior-art review found that spiralcheck, constraint-gauge, winding-ruler, tifxyz-doctor and sheetcheck already cover much of the obvious diagnostic space. winding-ruler reports that accurate pair-label estimators can still degrade real fits. We will not spend this session claiming another surrogate annotation ranking win.

The bounded engineering target is the current production-compatible optional fiber-direction extraction stage in ScrollPrize/villa, pinned to 4accc199a55695ebbefaab4fb6a99faa800fcabf. It is NOT enabled by default and this work does not claim its orientation loss improves reconstruction. Its CPU extractor materializes coordinates for every voxel, sorts accepted samples by cell, retains all chunk outputs, and concatenates them before serialization. We will attempt exact-output acceleration and bounded-memory serialization. A successful result establishes a data-preparation improvement, not better sheet identity, new ink, measured human-time savings, or a full spiral-fitting success.

## Mathematical contract
Within each global integer cell of edge c, among voxels in a half-open valid ROI with presence >= threshold, return the voxel with maximum presence; ties use smallest original C-order flat index. Return cells in lexicographic z,y,x order. For official uint8 inputs every selected index, coordinate, direction byte and confidence byte must match the pinned source exactly. Input coordinates/scales and sampling policy must not change. Missing chunks retain the original fill behavior. Empty requested regions must produce a valid empty artifact or a clear documented error, never silently fabricate samples. No change to learned model, loss, threshold or geometry is permitted.

## Data discovery rule, frozen before downloading prediction chunks
Use all four fiber prediction roots recorded in the public S3 catalog snapshot obtained during the source audit: PHercParis4 / 20260411134726, PHerc0332 / 20251211183505, PHerc1299 / 20260309130042, PHerc0139 / 20260102150214, all model 20260801084232 at L1. Retain exact manifests, array metadata and content hashes. Metadata/schema inspection is permitted; no test based on performance may change which cases are included.

For each root list presence chunks. Select up to eight existing chunks by SHA256('vesuvius-e1:'+full_chunk_key), restricted only by a recorded acquisition byte cap. Use the first selected Paris4 chunk for development; remaining chunks are confirmation. If complete bucket listing is impractical, use a documented deterministic spatial stratum listing and report the altered sampling frame before results. No sampled-case replacement based on foreground fraction, accuracy, runtime or favorable speedup. Unreadable/corrupt chunks are errors, not exclusions hidden from the table. Preserve compressed originals and hashes. Record cross-scroll inputs as independent source volumes, not independent scientific efficacy replication.

## Comparators
1. Unmodified pinned _cell_argmax.
2. Threshold-first sparse lexsort, a simple strong alternative removing unnecessary dense coordinates.
3. Regular-cell block reduction with deterministic tie behavior.
4. A small hybrid only if its dispatch criterion is fixed from the development chunk and synthetic development cases, before confirmation.
Use identical decoded arrays, dtype, global origins, ROI, cell size and threshold. Include full-array and clipped/misaligned ROI checks. Primary c=2, threshold=160 (upstream defaults). Sensitivity c in {1,2,4,8}, threshold in {0,80,160,240,255}; timing primary only plus a declared sensitivity subset.

## Correctness and adversarial tests
Direct scalar oracle independent of vectorization; random small shapes and cell/ROI alignments; all ties; zeros; empty arrays; no accepted samples; C/F/noncontiguous input; odd boundary chunk shapes; cells crossing input origin; large coordinate offsets; exact flat-index reconstruction; input non-mutation. Fail closed on unsupported values rather than claim equivalence outside tested dtype semantics. Monkeypatch only the selection function in the actual extractor for component isolation. Then test full staged-output integration against original extracted NPZ arrays and metadata on a local HTTP mirror of immutable real source chunks. Test output loader compatibility, zero-work behavior, I/O failure cleanup, output overwrite protection, ordering and bounded producer concurrency. These HTTP mirror tests isolate computation, not public-network speed.

## Performance
Local and clean GitHub CPU environment. Pin installed NumPy and dependencies for reproduction. One process per measured case/method; fixed thread counts; record CPU/Python/dependency versions. Warm up once and record five interleaved repetitions per confirmation case. Save per-case elapsed time, selected count, output digest and peak RSS. Compute per-volume medians and paired ratios; do not call repeated timings independent data. Report small/sparse regressions, absolute times, and peak RSS as well as ratios. Report both selection-only and full local-mirror extraction (decode, selection, output) so algorithmic timing is not passed off as end-to-end. Selection arrays must be exact before performance is considered.

## Acceptance gates
Exact primary outputs for every readable confirmation chunk and all oracle tests; no silent changed tie/ROI/coordinate semantics; tangible resource improvement on real cases against both legacy and a strong simple baseline, or report a negative result. Publish all per-case records. Independent machine must reproduce correctness and execute the code; timing need not match. If the more complicated method does not beat the simpler baseline, ship the simpler method. Record remaining unknowns explicitly.

## Not part of this claim
No qualified annotator has provided timing data. No authenticated GPU execution backend is currently connected; a Runpod connector was surfaced but no paid instance is provisioned. The unmodified full production optimizer is not claimed to have run. Production geometry quality and expert human-cost gates remain unpassed unless separately executed and documented. CPU-compatible upstream modules may be executed for integration tests without calling that a full scroll fit.
