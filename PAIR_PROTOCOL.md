# Equal-sized winding queries: secondary experiment

Registered 2026-09-09 after viewing collection-count and point-cost results, before running this pair experiment.

The original 32-collection comparison is cost-confounded: mean IVAR queries contain 663.225 original annotated points, versus 282.7 for random. Greedy gain-per-point selection under a 256-point cap performed worse than random. These negative findings must remain in the report.

## Revised action
Each acquired annotation is a disjoint pair of points from an existing relative-winding collection, asking for their relative winding difference. Every query costs exactly two point labels. Construct pairs from successive retained points, pairing indices (0,1),(2,3),...; points are not reused across pairs. Collections retain at most sixteen geometry-selected evenly spaced points, matching the original reduced estimator. A pair may span omitted intermediate points. Equal label count does NOT establish equal human time: counting intervening layers may vary in difficulty.

## Experiment
Keep the same reduced field, feature construction, all same/absolute base evidence, and eight shared initial full relative collections. All candidates come from the remaining training-side collections. Entire test collections remain inaccessible. Convert each two-point difference into a normalized Helmert contrast; use sigma=0.3 as before. Select random, chronological, spatial coverage, posterior variance/information, or output-weighted IVAR. All select precisely 8,16,32,64 pairs. Primary budget: 64 pairs = 128 acquired point labels.

Pilot splits: seeds 0,1,2. Fresh replay splits: 400–439. Spatial relative-collection holdouts: seeds 500–519. Shared same/absolute evidence remains available, including in the spatial test bands. No hyperparameter tuning is planned. Candidate acquisition sees geometry and covariance only, not unrevealed pair labels or test data. Risk averages geometry-side centered prediction error over candidate collections, as in the original benchmark.

This is a secondary, post-discovery design change, not the original preregistered primary experiment or an independent-scroll replication. Report every policy and budget, including failures. Correlated human errors and annotation time are unmeasured. No production-fitter or ink-recovery claim follows automatically.
