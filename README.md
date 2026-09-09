# Vesuvius annotation-selection research

Executed real-data research on public PHercParis4 annotations and reference surfaces, September 9, 2026. See **[RESULTS.md](RESULTS.md)** for the experiment designs, negative results, statistical caveats and conditional mathematical proof.

## What is demonstrated

| Experiment | Same-budget result | Important boundary |
|---|---|---|
| Surface resampling on 40 held-out patches | IVAR 7.4204 versus random 10.7352 native-voxel RMSE: **30.88% lower** | Existing UV/mask supplied; not unknown sheet discovery; tied with spatial coverage |
| Long-range winding questions, 40 replay splits | IVAR 1.3462 versus random 1.8388 winding RMSE: **26.79% lower** at 128 endpoint labels | Reduced model, not production spiral fitter; human time unmeasured |
| Spatial relative-collection holdouts, 20 splits | IVAR 1.8555 versus random 2.1506: **13.72% lower** | Shared same/absolute prior evidence remains available |

Information gain performed slightly better than IVAR. The original whole-collection experiment was cost-confounded; a gain-per-point variant failed. Those findings are retained, not hidden.

**No full-scroll reconstruction, new letters, ink-area improvement, actual expert-baseline win, prize acceptance or payment is claimed.**

## External reproduction completed

[Successful separate-CPU execution](https://github.com/Kkb113/research/actions/runs/34338465585): all **18 tests passed**, and all **12 aggregate numerical checks matched**, with maximum aggregate difference `5.5067062021407764e-14`.

- [Verification and environment](results/external_verification.json)
- [External aggregate results](results/reproduction_summary.json)
- [Complete external outputs](external_results.zip), including per-case errors and selected query coordinates
- [Test output](results/tests_after.txt)
- [Pinned source-data provenance](provenance)

This is computational reproduction on a second machine, not independent AI agents or independent-scroll scientific replication. Parallel numerical workers were used.

## Reproduce

Use Python 3.13; the reference runs used 3.13.5. The complete CPU benchmark does not require PyTorch or CUDA.

```sh
python -m pip install -r requirements.txt
python src/acquire.py --root .
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/test_research.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/run_confirmations.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python src/analyze.py
```

To audit the archived numerical results without rerunning all fits, execute `src/analyze.py` after data acquisition; it extracts `external_results.zip` when needed. The manifest-checked downloader rejects changed public data instead of silently substituting newer files. The initial acquisition Actions artifacts are temporary; manual reproduction uses committed provenance and public URLs, not those expiring artifacts.

## Protocol and implementation

- [Original protocol](PROTOCOL.md), frozen before its confirmation outcomes
- [Equal-sized pair protocol](PAIR_PROTOCOL.md), after discovering the cost failure
- [Long-range confirmation protocol](SPANNING_PROTOCOL.md), after three development pilots
- `src/winding_replay.py`: reduced field and block covariance updates
- `src/pair_replay.py`: disjoint adjacent/long-range questions
- `src/surface_replay.py`: given-UV reference-surface resampling
- `src/cost_replay.py`: original-point-budget negative control
- `src/extra_pair_baselines.py`: longest-first and span-matched random diagnostics
- `src/analyze.py`: conditional spatial-cluster bootstrap intervals
- `src/test_research.py`: algebra, provenance, disjointness and label-leakage tests

The published upstream Vesuvius source inspected was pinned to `4accc199a55695ebbefaab4fb6a99faa800fcabf`; it was not modified or run as the production fitter.

## Data attribution

Data: **Vesuvius Challenge — CT Scans of Herculaneum Papyri**, Giorgio Angelotti and collaborators; public PHercParis4 curated spiral inputs. [Dataset terms and citation requirements](https://scrollprize.org/data): **CC BY-NC 4.0 unless individual assets specify otherwise**. Third-party data and upstream code are not relicensed by this repository.
