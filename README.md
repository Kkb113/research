# Vesuvius annotation-selection research

Work initiated 2026-09-09. This repository records reproducible experiments, including negative results, on choosing winding annotations.

## Claim boundary
No improvement to the production Vesuvius spiral fitter is established yet. Synthetic uncertainty reduction is not reconstruction accuracy. Real-data replay with a reduced model must be reported as such. No prize or payment is claimed.

## Planned evidence
- Pin and hash public annotation data and upstream code.
- Keep entire annotation collections together when splitting train/query/test.
- Compare equal-budget random, geometry coverage, information gain, and risk-reduction policies using the identical estimator.
- Report held-out errors, paired uncertainty estimates, sensitivity and failure modes.
- Independently verify matrix formulas against direct recomputation.
- Do not use held-out annotation values for acquisition.

Public data remain subject to their original licenses. Code in this repository does not transfer rights in third-party data.
