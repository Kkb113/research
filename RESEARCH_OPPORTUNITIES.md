# Research opportunities: where a valuable Vesuvius contribution is possible

Assessment date: 9 September 2026. Ranking is a qualitative engineering judgment about credible utility, prior coverage, evaluability and available resources, not a prize prediction. Public searching cannot rule out unpublished work. No maintainer/annotator feedback has yet validated this ranking.

## Decision

The largest scientific opportunity remains trustworthy automatic **constraint generation and incorporation**, evaluated in the actual fitter under human-time budgets. The feasible delivery selected here is **exact resource-conscious fiber preprocessing**. Its scientific ceiling is lower, but it has a directly executable production code path, real cross-scroll inputs, an exact correctness contract and a small integration surface. We choose that bounded contribution rather than manufacture another surrogate ranking win.

The original IVAR project is not ranked first. Information gain slightly beat it, simple coverage nearly tied it, candidate traces were given, and true annotation cost was unmeasured. Winding-ruler supplies closer production prior art; spiralcheck already covers many generic evaluation ideas.

## Research coverage

We consulted official [open problems](https://scrollprize.org/2026_open_problems), [winding constraints](https://scrollprize.org/open_problems/winding_annotations), [spiral fitting](https://scrollprize.org/tutorial_spiral), [ink detection](https://scrollprize.org/tutorial5), [community projects](https://scrollprize.org/community_projects), prize descriptions, relevant primary literature and targeted production code. The pinned ecosystem audit fetched 213 source files and snapshots of recent issues, pull requests and commits. This is not a claim to have independently audited every line. The relevant upstream revision is [villa 4accc199](https://github.com/ScrollPrize/villa/tree/4accc199a55695ebbefaab4fb6a99faa800fcabf).

## Ranked opportunities

Each card specifies current evidence/coverage, potential novelty, data/compute/humans, difficulty, objective evaluation, integration, cross-scroll scope, benchmark-only risk and expected utility.

### 1. Constraint trustworthiness and production usefulness

**Evidence/coverage:** Official winding needs and [winding-ruler](https://github.com/pscamillo/winding-ruler), which reports good adjacent-label estimates but three generators degrading real fits. Existing work is substantial; accurate labels alone are not a new production result.

**Contribution/novelty:** Detect harmful, redundant or over-weighted relationships before incorporation. Known robust estimation/design; new value would be a measured Vesuvius failure taxonomy and corrective integration. **Resources:** predictions, annotations, checkpoint, independent geometry, GPU fits and qualified candidate adjudication/timing. **Difficulty:** high engineering, very high validation. **Evaluation:** same fitter/compute/human minutes, existing-generator and expert baselines, held-out identity, switches and valid area. **Integration:** input catalog/loss boundary, medium-high difficulty. **Cross-scroll:** high potential. **Benchmark-only risk:** high. **Expected utility:** very high if production gains survive; not demonstrated here.

### 2. Exact resource-conscious fiber evidence extraction — delivered E2

**Evidence/coverage:** Pinned `fiber_direction_samples.py` materializes voxel-wide coordinates, sorts candidates, retains outputs and concatenates them. E2 measured that actual stage. The optional orientation loss is off by default, limiting its reach.

**Contribution/novelty:** Ordinary block argmax and optional streamed NPZ serialization with unchanged evidence semantics. Vesuvius-specific engineering and empirical validation, not new mathematics. **Resources:** four public prediction volumes, CPU, codecs and spool disk; no human labels or GPU required for this claim. **Difficulty:** moderate. **Evaluation:** exact indices/bytes/schema, scalar oracle, strong sparse-sort baseline, full extraction entry point and original loader, time/RSS. **Integration:** small hash-checked patch; low difficulty. **Cross-scroll:** compatibility demonstrated on four volumes. **Benchmark-only risk:** low for this stage, high if generalized to geometry. **Expected utility:** moderate, directly deliverable; not a major unwrapping breakthrough.

### 3. Annotation provenance and human-effort instrumentation

**Evidence/coverage:** [spiralcheck](https://github.com/Nicodol/spiralcheck) documents resampled paths and missing generation-mode information in one point set; our endpoint budget cannot establish effort. Existing geometry exports do not supply a timing study.

**Contribution/novelty:** Record clicked/generated/corrected provenance, frame, active time, rejection and confidence in VC3D. Logging is established; real effort data would be the contribution. **Resources:** session instrumentation, consented qualified users and fixed tasks; CPU logging, GPU only for outcome studies. **Difficulty:** moderate coding, substantial human study. **Evaluation:** accepted independent evidence per minute including failures; compare unmodified tool. **Integration:** existing exports/UI, medium difficulty. **Cross-scroll:** high. **Benchmark-only risk:** medium. **Expected utility:** high enabling infrastructure, unvalidated here.

### 4. Independent cross-scroll evaluation evidence

**Evidence/coverage:** Spiralcheck already scores output meshes and audits geometric leakage; its own documentation limits the independence of existing producer runs. Repeated Paris4 splits are not different scrolls.

**Contribution/novelty:** Curate independently adjudicated regions with absolute identity, source provenance and geometric separation from fit inputs. Dataset contribution, not a new distance metric. **Resources:** different scroll geometries, trusted registration, qualified reviewers; CPU curation and GPU comparable fits. **Difficulty:** high, especially annotation. **Evaluation:** reviewer disagreement, independent producers, fixed holdouts; never assume generated meshes are physical truth. **Integration:** reuse spiralcheck formats, medium difficulty. **Cross-scroll:** central objective. **Benchmark-only risk:** low if others use it. **Expected utility:** high.

### 5. Explain combinations of reconstruction alarms

**Evidence/coverage:** Spiralcheck reports correlated metric responses to defects; one alarm does not uniquely identify one failure. Generic dashboards already exist.

**Contribution/novelty:** Abstaining diagnosis of winding offset, collapsed gap, misplaced sheet and boundary artifact from combined signals. Known classification/rules; new value is real-error localization. **Resources:** exported fits, independent defect labels, CPU and expert adjudication. **Difficulty:** medium engineering, high validation. **Evaluation:** simple-rule and single-alarm baselines plus blinded diagnosis, not planted defects alone. **Integration:** existing reports, medium. **Cross-scroll:** plausible, untested. **Benchmark-only risk:** high on artificial faults. **Expected utility:** medium-high.

### 6. Minimal-review contradiction sets

**Evidence/coverage:** Villa already ships `find_inconsistent_windings.py`, graph cycles and visualization. A nonclosing loop detector is not novel.

**Contribution/novelty:** Identify a small interpretable review set, separating gauge ambiguity from inconsistent evidence. Known graph diagnosis/robust optimization. **Resources:** patch graph, annotations, transforms, CPU plus GPU transform access and expert correction timing. **Difficulty:** medium-high. **Evaluation:** existing debugger, localization precision, retained correct evidence and repair minutes. **Integration:** medium. **Cross-scroll:** high potential. **Benchmark-only risk:** high with injected errors only. **Expected utility:** medium-high.

### 7. Generate questions directly from CT/geometry

**Evidence/coverage:** Official winding requirements and the curated-pool limitation of our replay. Villa already includes overlap connection and track-generation tools.

**Contribution/novelty:** Propose reviewable bridges between weakly linked components, including rejection evidence. Known geometry/graph proposals; validated candidate quality and cost would be new. **Resources:** correctly framed CT crops, predictions, graph state, CPU proposals, GPU inference/fits and qualified review. **Difficulty:** high. **Evaluation:** overlap connector, nearest/longest bridges and experts; accepted useful constraints per minute followed by production changes. **Integration:** high. **Cross-scroll:** high potential. **Benchmark-only risk:** high. **Expected utility:** very high if reliable, not established.

### 8. Conservative sheet-switch repair

**Evidence/coverage:** Official meshing failure list, existing surface/CT checkers and reported issue 1641. Detection is already being studied; continuity alone cannot establish physical identity.

**Contribution/novelty:** Reversible local repairs with independent evidence and abstention. Known optimization; new value is proven repair correctness. **Resources:** real faulty meshes, neighbors, raw CT, GPU fitting and substantial expert adjudication. **Difficulty:** very high. **Evaluation:** current correction workflow and deletion/abstention controls; true repaired area and introduced errors. **Integration:** high. **Cross-scroll:** plausible. **Benchmark-only risk:** very high on synthetic defects. **Expected utility:** very high with low near-term confidence.

### 9. Topology-aware prediction in difficult regions

**Evidence/coverage:** Official compressed/curved-region localization failures; strong nnU-Net and topology-aware prior work.

**Contribution/novelty:** Better localized labels or calibrated predictions specifically in difficult regions. Adding clDice/U-Net alone is not novel and tube guarantees do not automatically apply to sheets. **Resources:** registered CT, expert labels and GPU training. **Difficulty:** very high compute and validation. **Evaluation:** strong existing predictors, downstream connectivity/switches, not Dice alone. **Integration:** medium-high. **Cross-scroll:** high potential. **Benchmark-only risk:** high. **Expected utility:** high if native topology improves.

### 10. Geometry/ink arbitration without circular scoring

**Evidence/coverage:** Ink tutorial documents depth/orientation dependence; existing offset sweeps already address simple cases.

**Contribution/novelty:** Compare plausible surfaces using separately held-out ink/fiber evidence with abstention. Known multimodal reasoning; new value requires leakage-resistant production validation. **Resources:** frozen ink model, competing geometries, raw/rendered volumes, GPU and independent readability review. **Difficulty:** high. **Evaluation:** depth sweeps and flips, false extra surface, untouched ink assessment. **Integration:** high. **Cross-scroll:** uncertain. **Benchmark-only/circularity risk:** very high. **Expected utility:** high but uncertain.

### 11. Human-cost-aware active annotation selection

**Evidence/coverage:** Existing project has reduced-model gains, slight information-gain superiority over IVAR and no timing. Winding-ruler is closer production prior art.

**Contribution/novelty:** Empirical completion/rejection costs combined with calibrated production utility. Bayesian/cost-sensitive design is known. **Resources:** qualified timed sessions, candidates, checkpoint, independent evaluation and GPU. **Difficulty:** high. **Evaluation:** every requested strong baseline and actual experts; timestamps are not expert behavior. **Integration:** medium-high. **Cross-scroll:** untested. **Benchmark-only risk:** very high. **Expected utility:** medium until both cost and production gates pass; not selected for another replay.

### 12. Flattening distortion and seam provenance

**Evidence/coverage:** Flatboi/SLIM are established production tools. A replacement flattening algorithm is not inherently useful.

**Contribution/novelty:** Preserve distortion/seam maps through rendering and label transfer to localize errors. Engineering, not invention of SLIM. **Resources:** paired meshes, UV maps, renderer outputs, mostly CPU and some expert review. **Difficulty:** moderate. **Evaluation:** existing SLIM/metadata checks, registration errors and invalid area. **Integration:** moderate. **Cross-scroll:** high. **Benchmark-only risk:** medium. **Expected utility:** medium.

### 13. Strict influence-mask memory control

**Evidence/coverage:** Villa's query-footprint function uses a minimum query chunk, so its nominal element budget is not strict for large footprints. This is code evidence, not a measured E2 production OOM.

**Contribution/novelty:** Exact two-axis distance tiling; known reduction. **Resources:** real captured spiral-space queries/footprints, CPU oracle and GPU latency/VRAM tests; no new labels. **Difficulty:** low-medium coding, medium validation. **Evaluation:** existing chunk tuning and GPU-native alternatives, actual interactive latency. **Integration:** easy. **Cross-scroll:** high potential. **Benchmark-only risk:** medium. **Expected utility:** low-medium until measured; MEMORY_PROTOCOL.md remains a proposal.

### 14. Silent data-conversion failures and already-fixed defects

**Evidence/coverage:** Issue 1738 already reports multipage TIFF corruption in two implementations. The pinned upstream commit already fixes a linked-fiber synchronization cascade.

**Contribution/novelty:** Targeted format checks and regression tests; credit existing reporters. Do not reimplement or claim discovery of merged fixes. **Resources:** real-format fixtures, CPU and maintainer semantics decisions; no new annotation study. **Difficulty:** low-medium. **Evaluation:** exact conversion/rejection behavior in both copies. **Integration:** easy-medium. **Cross-scroll:** high. **Benchmark-only risk:** low. **Expected utility:** modest maintenance, not a major breakthrough.

## Gate conclusion

E2 passes a narrower exact-output preprocessing gate. Human-cost, full-optimizer, sheet-switch, readable-area and expert-comparison gates remain unpassed. Future high-impact work should build on winding-ruler and spiralcheck, collect actual effort/adjudication data, and test candidate trustworthiness rather than force IVAR to remain the answer.
