E10 verified summary package

These tables were independently reconstructed from e10_state_feature_families_results (2).zip.
The source archive contains 300 fit records, 300 per-state files, and 300 saved models,
but no aggregate, contrast, or completion summary files. All raw fits are complete;
no training needs to be repeated to recover the summaries.

Verified: 10 products x 3 seeds x 10 conditions; 120 E9 static/full anchors and 180 new
fits; dataset and implementation identifiers; state/model hashes; raw-state metric
means; E9 anchor provenance and exact metrics; 30 finite epochs for all 150 MLP fits;
250 boosting rounds for all 150 XGB checkpoints. A completion report identifies the
source archive checksum. This package contains summaries only; retain the original
source archive for raw states, models, feature definitions, and protocol metadata.

Averaging and inference
Training seeds are averaged within each product. The ten products are weighted equally.
The six planned Full-minus-intermediate Hits@1 contrasts share one Holm correction family.
Exact two-sided sign-flip tests assume product-level sign exchangeability. Overlapping
LOPO training sets and only ten products limit population inference. Bootstrap intervals
are descriptive and are not adjusted for multiplicity. Hits@3/MRR, stage, singleton,
and leave-one-product-out analyses are supporting/descriptive. A nonsignificant difference
does not establish equivalence. State-feature ablations identify conditional predictive
contributions under a frozen-family design, not physical causality.

Findings
Hits@1 is 35.96/37.98% for Static MLP/XGB, 35.98/37.93% for GlobalOnly,
35.98/38.07% for GlobalStatus, 41.12/43.34% for GlobalStructure, and
41.49/43.27% for Full. GlobalStructure updates global fractions and local degree/type
summaries while keeping explicit local activity/completion inputs frozen.
Full exceeds GlobalOnly and GlobalStatus for both learners (Holm p=0.0234375).
Full also exceeds GlobalStructure for MLP by 0.369 percentage points (Holm p=0.0234375).
For XGB, Full minus GlobalStructure is -0.069 percentage points (Holm p=0.53125).
Thus local degree/type updates carry most of the observed gain in this design;
activity/completion updates add a smaller conditional MLP benefit and no established
additional XGB benefit. Effects can include feature interactions; degrees and fixation
types were varied together and their separate contributions remain unresolved.

Representation-audit implications
E9 already showed the state-informed non-graph baselines above the tested DynamicReal
GNN on average. E10 identifies the useful information more precisely. It supports a
bounded representation-audit contribution; it does not establish general GNN inferiority,
a first-study novelty claim, physical planning feasibility, or Q1 submission readiness.
E11 remains the planned adjacency-alignment test with canonical activity/degree controls.
The close-literature comparison must establish how the joint audit differs from prior work.
