# Prior-art and novelty audit

Reviewed 9 September 2026. Searching public sources does not rule out unpublished work. Community results below are attributed reports, not experiments independently reproduced by E2.

## Unwrapping and geometry

Henderson, [Virtually Unrolling the Herculaneum Papyri by Diffeomorphic Spiral Fitting](https://arxiv.org/html/2512.04927v1), WACV 2026, is the closest methodological foundation: global spiral geometry, feature paths, deformation fitting and winding-aware evaluation. Model continuity does not establish correct native sheet identity. Our current optional fiber-direction extractor is a particular production implementation, not the paper's entire feature pipeline. [ThaumatoAnakalyptor](https://github.com/schillij95/ThaumatoAnakalyptor) also supplies automatic unwrapping and winding-aligned mesh-quality prior art. [SLIM](https://igl.ethz.ch/publications/igl-bibtex.php), Rabinovich et al. 2017, is established locally injective flattening. Neither nearest-surface evaluation nor distortion minimization is a new idea.

The official [open problems](https://scrollprize.org/2026_open_problems), [spiral tutorial](https://scrollprize.org/tutorial_spiral), [ink tutorial](https://scrollprize.org/tutorial5), [community projects](https://scrollprize.org/community_projects) and [prize examples](https://scrollprize.org/winners) help identify needs and integration points. They do not certify this contribution's value or award prospects.

## Existing Vesuvius work changes the research decision

[winding-ruler](https://github.com/pscamillo/winding-ruler), README blob `6b8d785dbad45056714a1f78ad4354d148953354`, reports production annotation-value studies and failed automatic constraint generators despite good local label accuracy. That directly challenges our old surrogate result. Its revised pitch interpretation also warns against confusing reproducible periodicity with a physical fundamental. Its numbers are not E2 findings.

[spiralcheck](https://github.com/Nicodol/spiralcheck), README blob `cde3b1c622d92a1cbc209dfcff5bbf898c377bbc`, already has CPU-only held-out geometry, winding/sheet consistency, intrinsic checks, leakage auditing and run comparisons. Its documented correlated alarms and limited independent-run evidence motivate targeted extensions, not a duplicate dashboard. Its path-sample provenance observations apply to the reported point set, not all annotations.

Neighboring constraint-gauge, windcheck, TIFXYZ Doctor, sheetcheck, ScrollAnchor and herculaneum-scroll-tools overlap with proposed verification/diagnostics. Their existence prevents broad novelty claims; we did not independently reproduce every implementation or conclude all problems are solved.

Pinned villa `4accc199a55695ebbefaab4fb6a99faa800fcabf` already contains winding-cycle diagnostics, path-based winding transport, overlap-derived connections, theta-crossing caches and interactive influence masks. These are essential baselines for new topology or candidate-generation work. Issue 1738's conversion problem and the current linked-fiber sync fix already have discoverers and implementation history.

## Experimental design and active learning

Cohn, Ghahramani and Jordan, [Active Learning with Statistical Models](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume4/cohn96a-html/statmodels.html), 1996: prediction-variance reduction is established. Our old rank-one formula is Gaussian conditioning, with model-conditional guarantees only.

Krause, Singh and Guestrin, [Near-Optimal Sensor Placements in Gaussian Processes](https://www.jmlr.org/beta/papers/v9/krause08a.html), 2008: information-based placement and approximation results are established. Their submodularity assumptions cannot silently be transferred to arbitrary IVAR objectives or human-cost/nonconvex reconstruction outcomes.

Joshi and Boyd, [Sensor Selection via Convex Optimization](https://web.stanford.edu/~boyd/papers/sensor_selection.html), 2009: subset selection, relaxations and performance bounds are prior art. A good Vesuvius application can be useful without new mathematics.

Sener and Savarese, [Core-Set Active Learning](https://arxiv.org/abs/1708.00489), 2017/2018: geometric coverage is a serious baseline. This supports the cautious interpretation of the earlier surface experiment where coverage nearly tied IVAR.

Konyushkova, Sznitman and Fua, [Learning Active Learning from Data](https://arxiv.org/abs/1703.03365), 2017: learned expected-error-reduction policies are established. Merely predicting candidate utility is not a new methodology.

Wang et al., [Cost-Effective Active Learning](https://arxiv.org/abs/1701.03551), and Gorriz et al., [Cost-Effective Active Learning for Melanoma Segmentation](https://arxiv.org/abs/1711.09168), supply related label-efficiency approaches. They do not provide timing data for winding annotation; fewer labels or more pseudo-labels cannot be counted as fewer expert minutes or independent physical evidence.

## Topology and segmentation

Shit et al., [clDice](https://openaccess.thecvf.com/content/CVPR2021/html/Shit_clDice_-_A_Novel_Topology-Preserving_Loss_Function_for_Tubular_Structure_CVPR_2021_paper.html), CVPR 2021, supplies established skeleton-based objectives for tubular/network-like structures. Fiber and sheet geometries differ; published guarantees must not be broadened without proof. Existing nnU-Net/topology-aware approaches must be strong baselines. A new loss must improve real connectivity, not only overlap scores.

## E2: exact distinction from the closest code

The direct comparator is `spiral-fitting/fiber_direction_samples.py`, SHA256 `48d0c7d3ea057e4d8fb7e2b8abece75906fca3067fbcc6e8cda963c13f8a5065`. It already defines the cellwise evidence sampling rule. E2 changes execution, not that evidence:

1. Ordinary block argmax replaces dense coordinates and sorting; threshold-first sparse lexsort remains a strong comparator and explicit fallback.
2. Optional ordered bounded futures and raw-file spooling avoid retaining/concatenating all selected output batches. Streaming NPY members into ZIP is known out-of-core engineering.
3. Exact coordinate/order/schema tests, real HTTP-mirror stage execution, source-hash checks and cross-machine output agreement make this a usable Vesuvius-specific component.

No invention of max pooling, blocking, sparse filtering, backpressure, NPZ, atomic publication or Bayesian design is claimed. No search proves that an equivalent optimization has never existed elsewhere. The defensible contribution is a compatible implementation and reproducible empirical resource behavior on the pinned stage.

| Claim type | Status |
|---|---|
| New mathematics/learning algorithm | Not claimed. |
| Known methods applied to an existing Vesuvius component | Implemented and tested. |
| Vesuvius-specific engineering | Coordinates, ties, order, schema, decoder/loader compatibility and patch. |
| New empirical finding | Exact-equivalence/resource results on the fixed four-volume corpus. |
| Physical sheet-identity or ink discovery | Not established. |
| Active selection usefulness per human minute | Not established. |

The result supports a bounded engineering contribution for technical review, not a major unwrapping breakthrough or an award claim.
