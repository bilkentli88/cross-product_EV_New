> Historical protocol documentation. The old XGB-only experiment labelled E9 here is supporting Supplementary Section S11.1, not the final principal E9. The current entry points are the root README and docs/reproducibility.md.

# Reproducibility guide

## 1. Scope and experimental unit

The manuscript evaluates reference next-operation ranking on 10 EV battery products under strict leave-one-product-out (LOPO) evaluation. In each fold, one complete battery is held out and all model fitting uses only the remaining products. The held-out battery product is the independent unit for statistical comparison.

Battery identity, raw component identifiers, raw fixation identifiers, and raw operation identifiers are excluded from the predictive representation. Categorical vocabularies are built from the training products only; unseen held-out categories map to an unknown token.

The target is the recorded immediate next operation among operations that appear later in the same recorded sequence. The dataset supplies one recorded sequence per battery, so this is a reference-ranking task rather than exhaustive physical-feasibility classification.

## 2. Canonical notebook sequence

### A. Initial cross-product baseline

`notebooks/historical/Battery_Disassembly_MLP_vs_GNN_LOPO.ipynb`

Compares the attribute-only MLP with the real-topology GNN under the common LOPO protocol.

### B. Capacity and preliminary topology ablation

`notebooks/historical/Battery_Disassembly_Topology_Ablation_LOPO_v2.ipynb`

Adds the capacity-matched MLP and the preliminary topology controls used to test whether parameter count alone explains the GNN advantage.

### C. Canonical static topology-mechanism audit

`notebooks/historical/Battery_Disassembly_Final_Topology_Mechanism_LOPO.ipynb`

Compares:

- `RealGNN`
- `NoEdgesGNN`
- five `ShuffledGNN` realizations

The historical `shuffle` label means semantic–topology permutation. A battery-specific node bijection is applied to both endpoints of each physical fixation edge, preserving the complete unlabeled graph up to relabeling while semantic attributes and operation-to-node references stay at their original semantic indices.

### D. Static input sensitivities

`notebooks/historical/Battery_Disassembly_No_Progress_Sensitivity_LOPO.ipynb`

Removes normalized sequence progress from the pairwise scoring head.

`notebooks/historical/Battery_Disassembly_No_Degree_Sensitivity_LOPO.ipynb`

Removes the three operation-local normalized degree features derived from the recorded physical graph.

Both sensitivities retrain the relevant conditions under the same LOPO folds and neural-training seeds.

## 3. Extended mechanism experiments

### E1 — test-time topology swap

`notebooks/historical/Battery_Disassembly_E1_Test_Time_Topology_Swap_LOPO.ipynb`

Purpose: determine whether a trained graph model actually uses the graph supplied at inference.

Forward intervention: a real-topology-trained model is evaluated on the recorded graph, each of the five semantic–topology permutations, and the no-edge graph with model parameters fixed.

Reverse intervention: each permutation-trained model is evaluated on its matched permutation and on the recorded physical graph.

Saved outputs: `results/historical/extended/e1_test_time_swap/`.

### E2 — global-context and structure-preserving controls

`notebooks/historical/E2_Global_Context_Controls.ipynb`

Conditions:

- real topology;
- no-edge;
- five semantic–topology permutations;
- global mean-pool context without adjacency;
- complete graph with one dummy edge type;
- five class-preserving rewired graphs.

The class-preserving rewiring retains node fixation degree, fixation-record identity/count, fixation edge type, and endpoint component-class pairing while changing exact adjacency.

Saved outputs: `results/historical/extended/e2_global_context/`.

### E2b — capacity-matched mean-pool

`notebooks/historical/E2b_Capacity_Matched_MeanPool.ipynb`

The context-branch width is increased from 64 to 85 so the mean-pool model is within 0.3% of the canonical GNN parameter count. The model still has no graph adjacency and no graph-branch physical degree.

Saved outputs: `results/historical/extended/e2b_capacity_matched_meanpool/`.

### E3 — stronger non-graph and heuristic baselines

`notebooks/historical/E3_Strong_Baselines_and_Heuristics_LOPO.ipynb`

Includes:

- XGBRanker with `rank:pairwise`;
- class-transition prior;
- graph-distance heuristic;
- shared-component continuation heuristic;
- analytical uniform-random baseline.

The XGBRanker uses product-invariant current/candidate operation descriptors, degree features, degree differences, categorical equality indicators, and normalized sequence progress, but no adjacency, component identity, product identity, or raw operation identifier.

Saved outputs: `results/historical/extended/e3_strong_baselines/`.

### E4 — training-budget sensitivity

`notebooks/historical/E4_Training_Budget_and_Convergence_LOPO.ipynb`

Real, no-edge, complete, and five permuted conditions are trained along the same trajectories and evaluated at 30, 100, and 300 epochs. The checkpoint comparison is diagnostic and is not used for retrospective epoch selection.

Saved outputs: `results/historical/extended/e4_training_budget/`.

### E5 — topology-dependent positive control

`notebooks/historical/E5_Positive_Control_Topology_Benchmark_LOPO.ipynb`

This benchmark retains the same products, LOPO protocol, model family, operation representation, ranking objective, and candidate sets but replaces the empirical next-operation target with a synthetic target constructed from one- and two-hop information in the true physical fixation graph.

Its role is methodological: if the audit cannot favor the real graph under a target deliberately generated from the real graph, an unsupported empirical real-versus-permuted comparison would be difficult to interpret. The benchmark is not intended as a realistic disassembly policy.

Saved outputs: `results/historical/extended/e5_positive_control/`.

### E6 — state-aware topology

`notebooks/historical/E6_Dynamic_State_Aware_Topology_LOPO_v2.ipynb`

This is the state-aware implementation used in the manuscript.

Conditions:

- `DynamicReal`
- five `DynamicShuffled` realizations
- matched `StaticReal`
- `DynamicComplete`
- `DynamicNoEdge`

#### State timing

Ranking state `t` is post-current-operation: operation `t` is applied before candidates for `t+1` are scored.

#### State update

- Executed fixation: remove the corresponding modeled fixation edge.
- Executed part operation: mark that part as removal-complete.
- Deactivate a removal-complete part only after it has no remaining **active incident modeled fixation**. The implementation checks that an unexecuted fixation has both endpoints structurally active before it counts as remaining.
- Retain inactive nodes in the fixed node index set as isolated semantic nodes so operation-to-node references remain stable.

#### Dynamic shuffled control

The same fixed node permutation is applied to the initial graph and every subsequent structural event. Operation-local semantic inputs and operation-to-node references remain at their original semantic indices. Therefore DynamicReal and DynamicShuffled have graph-isomorphic evolving structural sequences up to the fixed relabeling while differing in semantic–topological correspondence.

The notebook explicitly checks equality of state active-node fractions, remaining-edge fractions, and operation-local inputs between real and shuffled conditions.

#### State batching

All state graphs for one battery are combined into a block-diagonal graph. Blocks are disconnected, so no message exchange occurs between ranking states; this is computational batching of statewise GNN evaluations.

Saved outputs: `results/historical/extended/e6_state_aware/`.

### E9 — complementary StateAwareXGBRanker

`notebooks/historical/E9_StateAwareXGBRanker_LOPO.ipynb`

The notebook reuses the fixed E3 XGBRanker hyperparameters and uses the same E6 post-current history-consistent state updates. It constructs explicit per-node state descriptors (activity, completion, remaining and executed fixation connectivity, remaining edge-type statistics), fixed-endpoint summaries and process-wide fractions. It runs 10 LOPO folds × 3 XGBoost seeds. Training uses all nonterminal remaining candidates; evaluation includes terminal singleton states. The baseline is **not architecture-controlled** against DynamicReal because the representations and learning procedures differ.

The distributed notebook contains **extended all-product integrity assertions** that compare every per-node normalized remaining degree to E6 and probe whether changes to future ordering leave current-state feature rows unchanged. These assertions are executable but no passing report was supplied with the saved run archive. They should be explicitly rerun against the downloaded KIT data before final certification.

Saved canonical source run: the later CUDA run in `results/historical/extended/e9_stateaware_xgb/`. Original notebook's metadata pins the base code to commit `21b931fc3d7e05ec0ae01ad8b032016fb7706969`. Saved file aggregation gives StateAwareXGBRanker Hits@1 ≈0.422515 and DynamicReal − StateAwareXGBRanker ≈−0.032222 (product-level two-sided exact sign-flip p=0.021484375). The comparison is analyzed separately from the four designated E6 GNN contrasts.

Use `python scripts/historical/check_stateaware_xgb.py` to independently check the saved E9 CSVs and match the stored E6 DynamicReal per-product results. **This verifies arithmetic and file completeness only.**

### E8 — same-manufacturer exclusion

`notebooks/historical/E8_same_manufacturer_exclusion_dynamic_topology.ipynb`

Affected held-out products:

- Chevrolet Spark
- Chevrolet Volt
- BMW 530e
- BMW 330e
- BMW i3

When a BMW product is held out, all other BMW products are excluded from training. When a Chevrolet product is held out, the other Chevrolet product is excluded. Only DynamicReal and five DynamicShuffled realizations are rerun.

Because this analysis has only five independent held-out products, the minimum attainable two-sided exact sign-flip value for five nonzero same-direction differences is 0.0625. The manuscript therefore treats E8 descriptively.

Saved outputs: `results/historical/extended/e8_manufacturer_exclusion/`.

## 4. Fixed randomization and canonical training configuration

Neural-training seeds: `17, 29, 43`.

Topology-permutation IDs: `1, 2, 3, 4, 5`.

For permutation ID `r` and battery ID `b`, the canonical permutation-generator seed is:

`20261119 + 10007*r + b`

Permutation generation is independent of the neural-training seed. The same battery/permutation assignment is reused across the three neural-training seeds.

Canonical neural settings:

- 30 epochs;
- AdamW;
- learning rate `2e-3`;
- weight decay `1e-4`;
- dropout `0.10`;
- eight sampled negatives per training state;
- one optimizer update per training battery per epoch;
- no early stopping or held-out-product model selection.

In ordinary nine-product LOPO folds, 30 epochs correspond to 270 product-level optimizer updates.

## 5. Evaluation

At each held-out decision state, all operations appearing later in the recorded reference sequence are scored. The metrics are Hits@1, Hits@3, and mean reciprocal rank (MRR), with Hits@1 treated as the primary endpoint.

Scores within `1e-8` are treated as tied. Metrics use expected values under uniform random ordering within a tied score group, preventing storage order from determining performance.

The final decision state has a single remaining candidate and is included in the primary evaluation. A deterministic sensitivity analysis removes its contribution without retraining.

### Analytical uniform-random expectation

For `n` candidates:

- Hits@1: `1/n`
- Hits@3: `min(3,n)/n`
- MRR: `H_n/n`

where `H_n` is the `n`th harmonic number. The values are averaged within held-out product and then equally across products, matching the model aggregation.

## 6. Statistical analysis

Neural-training seeds are averaged within held-out product. Repeated graph controls (permutations, dynamic shuffles, rewiring realizations) are also averaged within product before product-level inference.

For designated product-level contrasts:

- mean paired product difference is reported;
- 20,000-replicate percentile bootstrap intervals summarize product-level uncertainty descriptively;
- inference uses an exact two-sided paired sign-flip test;
- Holm adjustment is applied within the designated Hits@1 family for each principal controlled experiment.

For `n=10`, all `2^10 = 1024` sign assignments are enumerated. Seeds and graph realizations are not inferential units.

The manuscript does not interpret an unsupported comparison as evidence of equivalence. In particular, the static real-versus-permuted result does not establish permutation superiority.

## 7. Matched reruns

Several extended diagnostics retrain a named canonical condition to provide a matched within-experiment comparison. Small numerical differences between repeated labels such as `RealGNN` across the canonical, E2, and E4 pipelines are therefore expected.

The formal DynamicReal-versus-StaticReal comparison uses the `StaticReal` condition rerun inside the E6 state-batched pipeline. It should not be replaced by the numerically separate canonical static result.

## 8. Result locations

See `results/README.md` for a file-by-file index. The main extended output directories are:

- `results/historical/extended/e1_test_time_swap/`
- `results/historical/extended/e2_global_context/`
- `results/historical/extended/e2b_capacity_matched_meanpool/`
- `results/historical/extended/e3_strong_baselines/`
- `results/historical/extended/e4_training_budget/`
- `results/historical/extended/e5_positive_control/`
- `results/historical/extended/e6_state_aware/`
- `results/historical/extended/e8_manufacturer_exclusion/`

## 9. Recomputing/checking summaries

Original canonical and no-progress statistics:

```bash
python scripts/historical/recompute_statistics.py
```

Compact consistency check for saved extended-experiment aggregates and contrasts:

```bash
python scripts/historical/check_extended_results.py
```

E9 result verification (no training):

```bash
python scripts/historical/check_stateaware_xgb.py
```

The notebook dataset finder defaults to `/content` for Google Colab. To run locally, configure the dataset search path; the external KIT dataset must be downloaded separately.

## 10. Interpretation boundary

The E6 graph is history-consistent with the observed reference prefix but is not a complete measured physical process state. The experiment does not establish closed-loop robotic feasibility, accessibility, collision-free execution, tooling availability, safety compliance, or optimal disassembly planning.
