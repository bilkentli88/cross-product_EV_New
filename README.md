# Physical Topology and Process State in Cross-Product EV Battery Disassembly Ranking

Reproducibility materials for the manuscript **“Physical Topology and Process State in Cross-Product EV Battery Disassembly Ranking: A Controlled Graph Audit.”**

## Study objective

The study asks how graph structure contributes to reference next-operation ranking on completely unseen EV battery products. It separates:

1. trainable-capacity effects;
2. generic structured cross-node computation;
3. correct physical semantic–topological alignment under a static graph; and
4. correct physical alignment when the graph is updated to reflect the executed disassembly history.

Evaluation uses strict leave-one-product-out (LOPO) validation over 10 battery products. The held-out battery product is the independent unit for statistical inference; neural-training seeds and graph-control realizations are repeated measurements and are not treated as independent samples.

## Main result in one paragraph

Under the canonical **static** representation, the real-topology GNN improves over no-edge and capacity-matched non-graph baselines, but correct physical alignment does not demonstrate an additional advantage over semantic–topology permutation controls. A topology-dependent positive-control benchmark verifies that the audit can detect correct topology dependence when it is present by construction. In the **state-aware** GNN experiment, the conclusion changes: `DynamicReal` outperforms `DynamicShuffled`, matched `StaticReal`, `DynamicComplete`, and `DynamicNoEdge` on all 10 held-out products for Hits@1. A complementary StateAwareXGBRanker reaches Hits@1 approximately 0.423 using explicit process-state features without learned graph message passing. The central interpretation is that correct physical semantic–topological alignment provides additional information within the matched state-aware GNN controls, while history-consistent state information can also be exploited through engineered tabular representations.

## Core experimental conditions

### Canonical static audit

- Attribute-only MLP
- Capacity-matched MLP
- Real-topology GNN
- No-edge GNN
- Five semantic–topology permutation controls

### Static mechanism and robustness diagnostics

- **E1:** test-time topology swap
- **E2:** mean-pool, complete-graph, and class-preserving rewired controls
- **E2b:** capacity-matched mean-pool control
- **E3:** XGBRanker and interpretable heuristic baselines
- **E4:** 30/100/300-epoch training-budget sensitivity
- no-progress sensitivity
- no-degree sensitivity
- terminal-singleton sensitivity

### Audit validation and state-aware extension

- **E5:** topology-dependent positive-control benchmark
- **E6:** state-aware topology experiment
- **E8:** same-manufacturer exclusion sensitivity
- **E9:** additional state-aware XGBRanker comparator (separate from the four matched E6 topology tests)

The manuscript does not use the exploratory E7 analysis.

## Important terminology

Historical notebook labels `shuffle`, `ShuffledGNN`, or `DynamicShuffledGNN` refer to **semantic–topology permutation controls**, not unconstrained edge rewiring. A battery-specific node bijection is applied to both endpoints of each fixation edge while semantic node attributes and operation-to-node references remain at their original indices. The unlabeled graph is therefore preserved up to node relabeling while semantic–topological correspondence is disrupted.

For E6, the same fixed permutation is applied consistently to the initial topology and every subsequent structural update. `DynamicReal` and `DynamicShuffled` therefore preserve the same evolving unlabeled graph sequence up to relabeling while differing in physical semantic–topological alignment.

## State-aware convention

At ranking state `t`, the recorded operation at position `t` has already been applied before candidate operations are scored.

- an executed fixation operation removes its modeled fixation edge;
- an executed part operation marks the corresponding part as removal-complete;
- a completed part is structurally deactivated only after no remaining **active incident modeled fixation** exists;
- inactive nodes remain in the node index set as isolated semantic nodes so operation-to-node references remain stable.

This is a deterministic, history-consistent representation of the recorded reference prefix. It is not a complete physical-feasibility model and does not directly encode geometry, accessibility, collision constraints, tooling, safety, graspability, or other deployment constraints.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── configs/
│   └── experiment_config.yaml
├── data/
│   └── README.md
├── docs/
│   └── reproducibility.md
├── notebooks/
│   ├── Battery_Disassembly_MLP_vs_GNN_LOPO.ipynb
│   ├── Battery_Disassembly_Topology_Ablation_LOPO_v2.ipynb
│   ├── Battery_Disassembly_Final_Topology_Mechanism_LOPO.ipynb
│   ├── Battery_Disassembly_No_Progress_Sensitivity_LOPO.ipynb
│   ├── Battery_Disassembly_No_Degree_Sensitivity_LOPO.ipynb
│   ├── Battery_Disassembly_E1_Test_Time_Topology_Swap_LOPO.ipynb
│   ├── E2_Global_Context_Controls.ipynb
│   ├── E2b_Capacity_Matched_MeanPool.ipynb
│   ├── E3_Strong_Baselines_and_Heuristics_LOPO.ipynb
│   ├── E4_Training_Budget_and_Convergence_LOPO.ipynb
│   ├── E5_Positive_Control_Topology_Benchmark_LOPO.ipynb
│   ├── E6_Dynamic_State_Aware_Topology_LOPO_v2.ipynb
│   ├── E8_same_manufacturer_exclusion_dynamic_topology.ipynb
│   └── E9_StateAwareXGBRanker_LOPO.ipynb
├── results/
│   ├── README.md
│   ├── paper_paired_statistics.csv
│   ├── random_baseline.csv
│   ├── individual_permutations.csv
│   ├── raw/
│   ├── sensitivity/
│   │   └── no_degree/
│   └── extended/
│       ├── e1_test_time_swap/
│       ├── e2_global_context/
│       ├── e2b_capacity_matched_meanpool/
│       ├── e3_strong_baselines/
│       ├── e4_training_budget/
│       ├── e5_positive_control/
│       ├── e6_state_aware/
│       ├── e8_manufacturer_exclusion/
│       └── e9_stateaware_xgb/
└── scripts/
    ├── recompute_statistics.py
    ├── check_extended_results.py
    └── check_stateaware_xgb.py
```

## Dataset

The experiments use:

**Baucks, M. and Morasch, A. (2026). Knowledge Graph Dataset of Product Structures and Disassembly Sequences of 10 EV Battery Packs. Karlsruhe Institute of Technology.**

DOI: https://doi.org/10.35097/emz24pksshndq468

The dataset is not redistributed in this repository. Download the archive from the DOI landing page and follow `data/README.md`.

## Environment

The notebooks use Python, NumPy, pandas, PyTorch, SciPy, scikit-learn, and XGBoost. Install the declared dependencies with:

```bash
pip install -r requirements.txt
```

A GPU is recommended for rerunning the full neural experiments. The notebooks can fall back to CPU, but the complete experiment suite contains many LOPO fits.

## Fixed canonical neural configuration

- LOPO folds: `10`
- neural-training seeds: `[17, 29, 43]`
- semantic–topology permutation IDs: `[1, 2, 3, 4, 5]`
- canonical epochs: `30`
- negative samples per training state: `8`
- optimizer: AdamW
- learning rate: `2e-3`
- weight decay: `1e-4`
- dropout: `0.10`
- categorical embedding dimension: `12`
- standard operation hidden dimension: `64`
- capacity-matched MLP width: `88`
- GNN hidden dimension: `32`
- edge-type embedding dimension: `8`
- message-passing layers: `2`
- tie tolerance: `1e-8`

For permutation ID `r` and battery ID `b`, the canonical permutation seed is:

```text
20261119 + 10007 * r + b
```

Permutation generation is independent of the neural-training seed.

## Selected manuscript-level results

### Canonical static audit

- Real-topology GNN Hits@1: approximately `0.293`
- No-edge GNN Hits@1: approximately `0.206`
- five-permutation mean Hits@1: approximately `0.330`
- Real − Permuted Hits@1: approximately `-0.037`, exact product-level `p=0.0605`
- Real − No-edge Hits@1: approximately `+0.087`, exact `p=0.00195`

The static result is interpreted as evidence for useful structured cross-node computation, not as evidence that permutation is superior or that physical topology is irrelevant.

### E5 positive control

- Real topology Hits@1: approximately `0.484`
- five-permutation mean Hits@1: approximately `0.128`
- Real − Permuted: approximately `+0.355`, positive on all 10 products

### E6 state-aware topology

- DynamicReal Hits@1: approximately `0.390`
- DynamicShuffled Hits@1: approximately `0.295`
- matched StaticReal Hits@1: approximately `0.279`
- DynamicComplete Hits@1: approximately `0.233`
- DynamicNoEdge Hits@1: approximately `0.205`

The four designated DynamicReal Hits@1 contrasts are positive on all 10 products and have Holm-adjusted `p=0.007812` within the E6 comparison family.

### E9 complementary state-aware non-GNN comparator

- StateAwareXGBRanker Hits@1: approximately `0.423`; Hits@3 approximately `0.605`; MRR approximately `0.542`.
- E6 DynamicReal Hits@1: approximately `0.390`.
- DynamicReal minus StateAwareXGBRanker: `-0.03222` Hits@1, exact paired product-level `p=0.021484375`; eight of ten held-out products favor StateAwareXGBRanker.
- This is a **model-and-representation comparison**, not an architecture-matched GNN ablation or a test of intrinsic superiority of one learning algorithm.
- E9 was reported separately from the original four-contrast E6 Holm family. The stored E9 run used XGBoost's CUDA device option; code can also run on CPU, but small numerical differences may arise.

### E8 manufacturer exclusion

Across the five affected BMW/Chevrolet held-out products, DynamicReal − DynamicShuffled Hits@1 is approximately `+0.078`, with DynamicReal higher on all five products. Because `n=5`, the minimum attainable two-sided exact sign-flip value is `0.0625`; this sensitivity analysis is interpreted descriptively.

## Statistical convention

The held-out battery product is the independent unit. Seeds, permutation realizations, rewiring realizations, and shuffle realizations are averaged within product before product-level inference. Hits@1 is the primary endpoint. Product-level bootstrap intervals are descriptive; exact two-sided paired sign-flip tests govern inference. Multiplicity adjustment is applied within the designated Hits@1 comparison family for each principal controlled experiment.

Where a diagnostic required retraining, canonical conditions were rerun within that diagnostic pipeline. Small numerical differences between repeated versions of the same named condition therefore reflect matched reruns. Inferential contrasts are always computed within the same experiment rather than across independently rerun pipelines.

## Reproducing reported summaries

For the original canonical statistics and no-progress sensitivity:

```bash
python scripts/recompute_statistics.py
```

For a compact check of the saved E1–E6/E8 result tables:

```bash
python scripts/check_extended_results.py
```

For an independent recomputation and consistency check of the saved E9 results against E6:

```bash
python scripts/check_stateaware_xgb.py
```

**Validation boundary:** these scripts audit *saved CSV outputs*; they do not retrain models. Reproducing model fits requires the external KIT dataset archive and notebook execution. The expanded E9 all-product feature-integrity assertions have not been independently confirmed from the shared result ZIP, which contains no printed audit report.

**Notebook paths:** most notebooks expect the KIT archive under `/content` in a Colab environment. Adjust their dataset-discovery path when running on a local machine; a local run is not guaranteed to work unchanged.

See `docs/reproducibility.md` for experiment-by-experiment details and `results/README.md` for output-file descriptions.

## Scope

The supervised target is the recorded reference next operation among operations appearing later in the same recorded sequence. The task is therefore **reference next-operation ranking**, not exhaustive physical-feasibility classification, optimal sequence generation, or closed-loop robotic planning.

## License

Repository code is released under the MIT License. The external dataset remains subject to the terms provided by its original publisher.
