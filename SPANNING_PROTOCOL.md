# Long-range two-point queries: registered secondary confirmation

2026-09-09. This extension follows the negative original point-cost control and the small positive adjacent-pair results. Three development splits (0,1,2) have now been viewed for a second geometry-only pairing rule. No other parameters were tuned.

## Pairing rule
For a collection's retained n points, query disjoint nested endpoint pairs (0,n-1),(1,n-2),... rather than adjacent pairs (0,1),(2,3),.... Every point belongs to at most one pair. Each pair is one relative-winding question with exactly two labeled endpoints. This provides long-range relationships without buying every intermediate label. Counting intervening layers could still cost more human time; equal endpoint count is not equal measured labor.

All methods receive the SAME spanning-pair candidate pool, initial annotations, estimator, and test collections. Candidate coordinates and relative order come from existing traces, so this is retrospective selection from available paths, not prospective discovery of trace locations. Acquisition never sees unrevealed winding values or test geometry.

## Frozen confirmation
Random whole-collection replay seeds 600–639; spatial relative-collection holdouts 700–719. Budgets 8,16,32,64 pairs; primary 64 pairs (128 newly acquired endpoint labels). Policies random, chronological, spatial coverage, information gain, and output-weighted IVAR. Same model settings and primary winding residual metric as PROTOCOL.md. Record per-query physical endpoint distance for cost diagnostics. Test exact disjointness and covariance update.

Report alongside adjacent-pair and failed whole-collection point-cost experiments, not instead of them. Same-scroll repeated splits are not independent-scroll replication. The interpretation remains reduced-field held-out label prediction; no production unwrapping, ink-area, measured human-time, or prize claim is established.
