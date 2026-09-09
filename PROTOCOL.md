# Experimental protocol — 2026-09-09

## Evidence boundary
This is a reduced-model study on real public PHercParis4 data, not yet a test of the production nonlinear spiral fitter or ink recovery. No breakthrough/prize claim is assumed. Report negative and positive results.

## Data
Public acquisition workflow runs: 34335967805 (annotation JSON), 34336125843 (upstream source/evaluation fibers), 34336322751 (48 deterministic surface patches). Each includes raw-file SHA256 manifests. Upstream pinned to 4accc199a55695ebbefaab4fb6a99faa800fcabf.

## Winding replay
254 nonempty relative collections; 125 nonempty same-winding collections and five nonempty absolute collections supply shared base evidence. Hold entire relative collections out, never individual points from a queried collection. Eight shared initial relative collections. Compare random, chronological creation-time replay, spatial farthest-point coverage, block information gain, and block integrated variance reduction (IVAR), with the identical reduced winding estimator. Chronological replay is NOT a claim to reproduce current expert behavior.

Pilot seeds 0,1,2 have been viewed. Pilot results favored both information criteria over random. Before confirmation, correct the angular convention to [0,2pi) and the integrated risk normalization to mean per-point error. Keep all parameter choices fixed: 96 RBF centers, spatial scales 700/700/2500 native voxels, observation sigma 0.3 winding units, a 25-voxel radial prior. These are assumptions, not calibrated physical constants.

Confirmatory seeds 100–139; budgets 8,16,32 additional collections. Primary outcome: mean over held-out collections of centered per-point squared winding residual, reported as RMSE. Secondary: mean absolute residual and fraction exceeding half a winding (NOT a directly observed sheet-switch rate). No test coordinates or test values are used to choose feature centers or score queries. Acquisition sees candidate design matrices only.

Controls: spatial z-block holdout; sensitivity to length scale, observation noise, and basis size; equal point-cost acquisition where feasible. Repeated splits share the same scroll and labels and are NOT independent scroll replicates. Statistical reporting must acknowledge that and include spatial/collection-level uncertainty where possible.

## Surface reconstruction benchmark
48 patch directories were selected by the lowest SHA256 of 'vesuvius-2026-09-09:' plus directory name from the full server listing, before viewing geometry. First eight are development patches; remaining forty are evaluation patches. Exclude only unreadable/nonfinite files or fewer than 96 valid XYZ vertices; report exclusions. The first three inspected patches belong to the development set.

Task: reconstruct held-out real XYZ coordinates from selected surface-grid samples, using a shared GP interpolator with a linear trend. The already-existing UV parameterization and validity mask are GIVEN. This is a reference-mesh resampling benchmark, NOT discovery of unknown sheet connectivity. Reference patches include algorithm-generated surfaces and are not independently verified CT ground truth.

Compare random, UV farthest-point coverage, maximum posterior variance, and IVAR. Queries use UV/mask geometry, never hidden XYZ. Each method starts with the same four geometry-selected seed points. Evaluate budgets of 4,8,16,32 additional points and actual held-out Euclidean position error, not posterior variance. Primary budget: sixteen additional points. Kernel starts as Matern-5/2 plus linear trend; any development-only tuning is recorded. Average random repeats within a patch before treating patches as statistical units. Check sensitivity and spatial correlation. Do not rename this benchmark as production global reconstruction.

## Verification
Test covariance/risk formulas against direct inversion; test label-blind selection; check exact source hashes and split disjointness; retain complete per-case results. An independent implementation of a calculation is a numerical cross-check, not an independent AI agent or independent scientific replication.
