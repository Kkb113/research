# Real-data results — September 9, 2026

## Established result and claim boundary

Two executed benchmarks now go beyond the original synthetic prototype. **These are not tests of the production nonlinear spiral fitter. No new ink, whole-scroll unwrapping, human-time savings, prize acceptance, or payment has been established.**

1. **Known-UV surface resampling:** IVAR lowered actual held-out XYZ error by **30.88% against random** on forty reference patches with equal twenty-point budgets. It was effectively tied with spatial coverage.
2. **Long-range winding queries:** IVAR lowered held-out centered winding error by **26.79% against random** on forty replay splits using equal 128-endpoint budgets, and **13.72%** on twenty spatially separated relative-collection splits. Information gain performed slightly better than IVAR.

## Reproduction already completed

[GitHub Actions run 34338465585](https://github.com/Kkb113/research/actions/runs/34338465585) completed successfully on a separate CPU environment. All **18 tests passed**, and all **12 aggregate numerical reference comparisons passed**. The largest aggregate difference was **5.5067062021407764e-14**. The separate run reproduced the negative cost result and stronger baselines too.

- `results/external_verification.json`: environment, source hashes, individual checks.
- `results/reproduction_summary.json`: external aggregate values.
- `results/tests_after.txt`: actual test output.
- `external_results.zip`: complete external experiment outputs, selections and per-case errors.
- `provenance/`: source URLs, SHA-256 hashes and deterministic patch sampling manifest.

This is same-code computational reproduction on a second machine, not independent scientists, independent AI agents or a new-scroll replication.

## Surface experiment

Forty evaluation patches were held apart from eight development patches. All forty met the predeclared validity criterion. Each patch used two point splits, a pool of at most 256 candidates and up to 512 held-out vertices. Every method received the same four corner-nearest initial samples. Uniform random selection had twenty repeats per patch/split: **1,600 random trajectories**.

All methods used the same Matern-5/2 plus linear-trend Gaussian-process interpolator. Selection saw UV/mask geometry and covariance, not unrevealed XYZ. The existing UV parameterization is PROVIDED: this is resampling an already represented surface, not discovering sheet connectivity in CT. Some public reference meshes have algorithmic provenance and are not independent physical ground truth.

| Method | Held-out XYZ RMSE at 20 total points, native voxels |
|---|---:|
| Random | 10.7351504581 |
| Spatial coverage | 7.4488199792 |
| Maximum variance | 7.5656932747 |
| IVAR | 7.4204301410 |

After averaging random repeats and both splits within each patch, IVAR improved over random on **40/40 patches**. The mean reduction was **30.8773%**, with a paired spatial-cluster bootstrap interval **28.75–33.01%** over thirty occupied spatial bins. Against coverage the reduction was **0.3811%**, interval **-5.48% to +5.58%**, with only 18/40 patch wins. **Superiority over coverage is not supported.** Alternative kernel scales changed the ordering of the informed selectors.

## Winding experiment and an important failed control

The public PHercParis4 files contained 254 usable relative collections, 125 same-winding collections and five absolute collections. Empty collections were excluded. The reduced field used 96 geometry-derived RBF features plus five global features, a radial/angle prior, assumed observation noise 0.3 winding units, and fixed geometry scales. These are assumptions, not calibrated physical constants.

Whole relative collections—not individual points—were held out. All methods shared same/absolute base evidence and eight initial relative collections. Test geometry was excluded from acquisition and feature construction. The metric is centered winding residual, **not an observed sheet-switch rate**.

At 32 additional whole collections, IVAR achieved RMSE 1.2024 versus random 1.8406. But IVAR acquired **663.225 original labeled points on average**, versus random's **282.7**. At a 256-original-point budget, greedy gain-per-point IVAR was **worse**: 2.0969 versus random 1.9230. This cost imbalance invalidates a simple claim of label efficiency from the original collection-count result.

## Revised equal-sized questions

Each question now asks for the relative winding difference of two endpoints. Retained points are paired without endpoint reuse: `(0,n-1), (1,n-2), ...`. Every method sees the same long-range candidate pool and acquires 64 questions, or **128 new endpoint labels**. Candidate trace geometry already exists; discovering those traces is not included in the measured budget.

Adjacent two-point queries were also tested and gave only small gains: 3.00% on random splits and 1.29% on spatial splits. Three development pilots for the long-range rule were followed by a public preconfirmation protocol (`SPANNING_PROTOCOL.md`), fixing seeds 600–639 and spatial seeds 700–719 before viewing those outcomes.

| Method | 40 random collection-holdout splits | 20 spatial relative-collection holdouts |
|---|---:|---:|
| Random | 1.8387593347 | 2.1505703220 |
| Recorded chronological order | 2.0944556706 | 2.3561869524 |
| Spatial coverage | 2.0117159519 | 2.2402571209 |
| Longest endpoints first | 1.4653921755 | 2.0529926849 |
| Span-matched random | 1.4190490425 | 1.9613233891 |
| Information gain | **1.3322400735** | **1.8528695275** |
| IVAR | **1.3462072495** | **1.8554591538** |

IVAR beat uniform random in **40/40** random splits and **20/20** spatial splits. Conditional spatial-cluster bootstrap intervals for the mean-RMSE reduction were **19.23–33.39%** and **8.69–19.14%**. The fitted models are held fixed while resampling spatial groups of held-out collections. These are one-scroll, conditional intervals, not independent trial or new-scroll generalization guarantees.

Longest-first and span-matched random were post-hoc controls. Span-matched random follows the decile distribution of IVAR-selected endpoint distances, with twenty repeats per random split and ten per spatial split. IVAR improved over longest-first by **8.13%** and **9.62%**, and over mean-RMSE span-matched random by approximately **5.13%** and **5.40%**. Pooling matched-random squared errors before taking RMSE, as used in the bootstrap, gives slightly different **5.25%** and **5.57%** estimates, with intervals **1.13–10.53%** and **2.92–9.14%**. The aggregation distinction is intentional and must not be silently mixed.

Information gain remains marginally better than IVAR. No claim of beating established information gain is supported. The contribution is the problem formulation and evidence that selecting nonredundant long-range relationships can matter at equal endpoint counts.

Equal endpoint count is **not equal human time**. Selected IVAR spans are longer than uniform random spans; verification may be harder. Spatial splits remove relative query collections but retain shared same/absolute base evidence, including in the test band. Absolute residuals around 1.35–1.86 windings remain too large to claim correct unwrapping.

## Exact mathematical statement

For Gaussian parameter uncertainty `C`, a candidate linear observation `A` with independent noise covariance `R > 0`, and output-loss weighting `M >= 0`:

```
C_new = C - C A^T (R + A C A^T)^-1 A C
Delta = tr((R + A C A^T)^-1 A C M C A^T) >= 0
```

The trace is a squared Frobenius norm. It is the exact decrease in the posterior mean's **modeled expected squared prediction loss**. Maximizing it over equal-cost candidates dominates the average one-step modeled gain of uniform random selection from the same current state.

This does not prove multi-step global optimality, realized-error improvement under misspecification, or better real scroll unwrapping. A numerical counterexample to the unconditional realized-error claim is included in the test suite. Variance-based active learning is established prior work, not a newly invented general theorem.

## Outstanding production validation

The official spiral fitter combines geometry and volumetric evidence into a deformed global spiral. Its documented GPU/Python requirements were not available in the local CPU environment. A decisive next validation must use the same frozen production fitter, independently collected candidate labels, measured human annotation time, matched optimization budgets and actual held-out geometry/ink metrics. An actual expert-selected baseline is required: chronological timestamps are not a substitute.

No prize submission or IP transfer has been made. All findings refer to one scroll and publicly available reference annotations.

## Sources and data terms

Data attribution: **Vesuvius Challenge — CT Scans of Herculaneum Papyri**, Giorgio Angelotti and collaborators; public PHercParis4 curated spiral inputs. Original data remain **CC BY-NC 4.0 unless individual assets state otherwise**. Third-party data and upstream code are not relicensed by this repository.

- [Winding-constraint priorities](https://scrollprize.org/open_problems/winding_annotations)
- [Spiral-fitting pipeline](https://scrollprize.org/tutorial_spiral)
- [Dataset attribution and licensing](https://scrollprize.org/data)
- [Cohn, Ghahramani and Jordan: Active Learning with Statistical Models](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume4/cohn96a-html/statmodels.html)
- [Joshi and Boyd: Sensor Selection via Convex Optimization](https://web.stanford.edu/~boyd/papers/sensor_selection.html)
- [Sellan and Jacobson: Stochastic Poisson Surface Reconstruction](https://www.dgp.toronto.edu/projects/stochastic-psr/)
