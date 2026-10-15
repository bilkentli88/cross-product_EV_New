> Historical saved outputs. The XGB-only E9 here is not the final principal E9. Current results are under results/principal/.

# Results index

The held-out battery product is the independent unit for inference. Neural-training seeds and graph-control realizations are repeated measurements and must not be counted as independent products.

## Canonical and original sensitivity outputs

Top-level files retain the structure of the original repository:

- `paper_paired_statistics.csv`: manuscript-level canonical capacity and static-topology contrasts.
- `random_baseline.csv`: analytical uniform-random ranking baseline.
- `individual_permutations.csv`: static permutation-specific diagnostics.
- `no_progress_sensitivity_paired.csv` and `no_progress_sensitivity_summary.csv`: no-progress sensitivity summaries.
- `raw/`: canonical seed-level and fold-level experiment outputs, including no-progress raw outputs.

## No-degree sensitivity

`results/sensitivity/no_degree/` contains:

- `no_degree_sensitivity_fold_mean.csv`
- `no_degree_sensitivity_paired.csv`
- `no_degree_sensitivity_paired_seed.csv`

This analysis removes the three operation-local normalized degree features derived from the recorded physical graph and retrains the relevant conditions.

## Extended experiment outputs

### E1 — test-time topology swap

`extended/e1_test_time_swap/`

Contains aggregate, fold-level, paired-seed, evaluation-level, contrast, and metadata files. The designated Hits@1 contrasts evaluate inference-time use of the supplied graph with model parameters fixed.

### E2 — global-context and structure-preserving controls

`extended/e2_global_context/`

Contains real, no-edge, five semantic–topology permutations, mean-pool, complete-graph, and five class-preserving rewired controls, together with rewiring diagnostics and product-level contrasts.

### E2b — capacity-matched mean-pool

`extended/e2b_capacity_matched_meanpool/`

Contains the width-85 mean-pool control and parameter-count diagnostics showing a maximum GNN parameter gap below 0.3%.

### E3 — stronger baselines and heuristics

`extended/e3_strong_baselines/`

Contains XGBRanker, class-transition prior, graph-distance heuristic, shared-component continuation heuristic, uniform-random baseline, candidate-size diagnostics, and contrasts.

### E4 — training-budget sensitivity

`extended/e4_training_budget/`

Contains checkpoints and summaries for 30, 100, and 300 epochs. The same training trajectories are evaluated at all checkpoints; the experiment is not used for retrospective epoch selection.

### E5 — topology-dependent positive control

`extended/e5_positive_control/`

Contains the deliberately topology-dependent benchmark used to verify that the audit can detect correct physical alignment when the ranking target is constructed from the true graph.

### E6 — state-aware topology

`extended/e6_state_aware/`

Contains aggregate, fold, seed, contrast, state-validity, graph-evolution, progress, edge-case, and metadata files for `DynamicReal`, five `DynamicShuffled` realizations, matched `StaticReal`, `DynamicComplete`, and `DynamicNoEdge`.

Important implementation convention: ranking state `t` is **post-current-operation**. A completed node is deactivated only after no remaining active incident modeled fixation exists.

### E8 — same-manufacturer exclusion

`extended/e8_manufacturer_exclusion/`

Contains the five affected BMW/Chevrolet product folds, fit-level results, control-validity checks, aggregate summaries, and product-level DynamicReal minus DynamicShuffled contrasts. Because the analysis has only five independent held-out products, inferential resolution is limited and the result is interpreted descriptively.

### E9 — state-aware XGBRanker (complementary)

`extended/e9_stateaware_xgb/`

Contains the canonical CUDA-run `stateaware_xgb_seed_results.csv`, `stateaware_xgb_fold_mean.csv`, `stateaware_xgb_aggregate.csv`, `stateaware_xgb_vs_dynamicreal_products.csv`, `stateaware_xgb_vs_dynamicreal_contrast.csv`, metadata and a run checkpoint copy. This additional feature-engineered XGBRanker analysis is kept separate from E6's matched GNN Holm family.

`python scripts/check_stateaware_xgb.py` independently verifies saved output consistency and the product-level exact sign-flip p-value. **It does not retrain models or independently certify that E9's all-product integrity assertions passed.**

The standalone `singleton_sensitivity.csv` and `structural_associations.csv` described in older repository drafts are not packaged in this snapshot. Some no-degree intermediary seed/partial files are likewise absent; see the actual `sensitivity/no_degree/` directory. Original analytical conclusions should not be confused with availability of those missing intermediate files.

## Matched reruns

Several diagnostic experiments independently rerun named canonical conditions in order to create a matched within-experiment comparison. Small numerical differences between, for example, canonical `RealGNN` and an E2/E4 rerun are expected. Do not combine values across independent pipelines for inferential contrasts; use the contrast files from the corresponding experiment.
