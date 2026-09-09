# Vesuvius research: exact evidence preprocessing and archived annotation selection

## Current contribution: E2 exact-output fiber preprocessing

A small, tested improvement to the actual optional `fiber_direction_samples.py` preprocessing stage. It preserves selected coordinates, ordering, direction/confidence bytes and parsed format-2 metadata while reducing CPU selection work and optionally output-serialization memory. **It is not a whole-scroll reconstruction, human-cost, sheet-switch or ink-recovery result.**

- [Results and retained regressions](RESULTS_E2.md)
- [Ranked research opportunities](RESEARCH_OPPORTUNITIES.md)
- [Prior-art and novelty audit](PRIOR_ART.md)
- [Integration and CLI](INTEGRATION.md)
- [Limits and unpassed gates](LIMITATIONS.md)
- [Frozen E2 protocol](E2_PROTOCOL.md)
- [Completed clean-machine reproduction](EXTERNAL_VALIDATION.md)

The clean CPU run reacquired all 112 original input files by public URL and checked their hashes. All 2,480 configuration comparisons and 155 saved selection arrays match the local execution. Nine unit tests pass, including a 480-case scalar-oracle test. At the primary setting, block selection is faster than upstream on 28/31 cases and a strong sparse-sort baseline on 23/31. Regressions remain recorded.

At 17,279,232 records in an explicitly repeated-real-batch serialization workload, total process peak RSS was 386.63 versus 97.05 MiB locally and 330.98 versus 39.09 MiB externally. This is a disk-for-memory tradeoff, not 128 independent regions. Small jobs can be slower with streaming.

```bash
python -m pip install -e .
bash scripts/reproduce_e2.sh
```

The manifest is losslessly encoded in `provenance/manifest.parts/*.b64`; acquisition verifies its frozen SHA256 and every original file. Reproduction does not depend on expiring Actions input artifacts. Generated results are written to `e2_results/`.

## Earlier annotation-selection work — preserved, not promoted

[RESULTS.md](RESULTS.md) contains the original PHercParis4 reduced-model and reference-surface experiments, conditional proof, cost-confounded result and failed gain-per-point control. Information gain slightly outperformed IVAR; coverage nearly tied IVAR on reference surfaces. Equal endpoint count was not measured human time. The 18 original tests and separate-machine numerical reproduction remain in `src/`, `results/`, `external_results.zip`, and the original [PROTOCOL.md](PROTOCOL.md), [PAIR_PROTOCOL.md](PAIR_PROTOCOL.md), [SPANNING_PROTOCOL.md](SPANNING_PROTOCOL.md).

Legacy reproduction uses `pip install -r requirements.txt`, `python src/acquire.py --root .`, `python src/test_research.py`, and `python src/run_confirmations.py` with single-threaded BLAS/OpenMP. The original protocols are intentionally not rewritten after their outcomes.

E1 engineering protocols also remain as an audit trail. Their unarchived local source was not recovered; E2 is a new explicitly frozen implementation, not a claimed reproduction of those missing hashes.

No GPU was provisioned, no qualified annotator study was performed, and no independent AI research agents, upstream acceptance, prize or payment are claimed. New code is MIT; third-party data retain their original terms. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
