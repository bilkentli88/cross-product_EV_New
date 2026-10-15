# Physical Topology and Process State in Cross-Product EV Battery Disassembly Ranking

Reproducibility materials for **Physical Topology and Process State in Cross-Product EV Battery Disassembly Ranking: A Controlled Representation Audit**, prepared for *Computers in Industry*.

## Main findings

This repository distinguishes explicit engineering-state summaries from graph message passing in teacher-forced reference next-operation ranking for ten EV battery products. An unordered remaining-operation inventory is supplied; the executed recorded prefix defines the current state. These are reference-ranking scores, not planning-success or physical-feasibility rates.

| Principal study | Question | Equally weighted product mean Hits@1 |
|---|---|---|
| E9 | State-aware learners and their initial-state feature controls | MLP **41.49%**, XGB **43.27%**, matched dynamic GNN **38.81%**; initial-state MLP **35.96%**, XGB **37.98%** |
| E10 | Which fixed-schema feature updates carry the improvement? | GlobalStructure MLP **41.12%**, XGB **43.34%**; Full MLP **41.49%**, XGB **43.27%** |
| E11 | Adjacency conditional on retained physical degree and semantic inputs | Real **38.54%**, five-realization ActiveShuffle **33.38%**, NoEdge **31.11%** |

E9's state-aware scalar pipelines exceed the tested GNN. E10 locates most improvement in jointly updated degree/type and global summaries; it does not separate degree and fixation-type contributions. E11 finds additional predictive value for correctly aligned messages within the tested GNN. Shuffled computational degrees can disagree with retained physical degree covariates, so E11 is a conditional correspondence test, not an isolated causal topology effect or evidence of general GNN superiority.

Products (n=10) are the comparison units. Seeds and realizations are averaged within product. Sign-flip tests assume product-level sign exchangeability; shared manufacturers and overlapping training folds limit population inference. Separate Holm families cover four E9, six E10, and two E11 Hits@1 tests. Bootstrap intervals are descriptive. E10 was selected after E9; internal prospective protocol locks are not external preregistration.

## Quick verification: no dataset, GPU, or retraining needed

```bash
python -m pip install -r requirements.txt
python scripts/verify_repository.py
python scripts/verify_saved_statistics.py
python scripts/verify_state_records.py
python scripts/regenerate_figures.py
```

These commands check packaged file provenance, recompute saved fit/product aggregates and primary exact/Holm tests, verify all 660 per-fit state-metric records, and regenerate the two result plots into `generated_figures/`. They do not train models or prove dataset-level physical validity. See [reproduction instructions](docs/reproducibility.md) and [the validation report](docs/VALIDATION_REPORT.md) for the checks actually run on this package.

## Final experiment notebooks

| Study | Notebook | Recorded study provenance |
|---|---|---|
| E9 | [State-aware baselines](notebooks/E9_State_Aware_Baselines.ipynb) | 150 fits |
| E10 | [State-feature families](notebooks/E10_State_Feature_Families.ipynb) | 300 records: 120 verified E9 endpoints plus 180 new fits |
| E11 | [Canonical-degree adjacency](notebooks/E11_Canonical_Degree_Adjacency.ipynb) | All 210 fits trained afresh after the all-or-none E9 reference gate failed |

These self-contained notebooks preserve their delivered executable code and bytes. Their setup defaults are **full training enabled for E9 and E11**, and **disabled for E10** until enabled in its full-run cell. Read the notebook settings before execution. Summary verification above is the fast inspection route. Notebook introductions describe their original preparation stage; the saved completion records and current README document the completed study.

## Repository contents

- `notebooks/`: the three final self-contained notebooks.
- `results/principal/e9`, `e10`, `e11`: saved protocols, every fit JSON and per-state metric CSV, diagnostics, and final summaries. Model weights are in the separate original exports.
- `results/audits/`: retained numerical audit and CPU sensitivity records.
- `notebooks/historical/`, `results/historical/`, `scripts/historical/`: earlier supporting experiments, kept separate from the principal protocols.
- `configs/`: current protocol summary, recorded software environments, and separately labelled historical settings.
- `provenance/`: original source archive hashes, notebook provenance, and packaged-file integrity manifest.
- `scripts/`: verification and figure-regeneration commands.
- `docs/`: reproduction, provenance, code-availability, and publishing instructions.

**Historical naming collision:** `notebooks/historical/E9_StateAwareXGBRanker_LOPO.ipynb` is the older XGB-only comparator (approximately 42.3% Hits@1), corresponding to Supplementary Section S11.1. It is not the final principal E9 (XGB 43.27%, MLP 41.49%). Earlier static and E6 graph perturbations also change degree/state context and must not be substituted for E11.

## Dataset and software

The external KIT dataset is available at <https://doi.org/10.35097/emz24pksshndq468>. It is not redistributed here. [Dataset instructions](data/README.md) list the four original CSV names and their SHA-256 hashes. Principal saved protocols record PyTorch 2.11.0+cu130 and NumPy 2.1.3; E9/E10 also record XGBoost 3.4.1 and scikit-learn 1.6.1. [Recorded environments](configs/recorded_environments.json) describe the original runs; `requirements-training.txt` is an installation convenience, not a guarantee of identical numerical output on every device or package version. Do not replace a working Colab PyTorch installation just to inspect saved CSVs.

## Original exports and checkpoints

The separate accompanying **EV_Final_Experiment_Exports.zip** contains four unchanged original archives: E9 exports, E10 original fit exports, separately verified E10 summaries, and E11 exports. It includes model checkpoints and full original state/fit/diagnostic exports. Archive hashes are listed in [source_archives.json](provenance/source_archives.json).

For public distribution, attach this large companion ZIP to a GitHub Release and link its actual published asset URL from the release/README. It is intentionally outside the small source ZIP. Until that upload is completed, do not describe the checkpoint archive as publicly hosted on GitHub. Source code and saved-state numerical checks are available from this repository alone once its cleaned contents are uploaded.

```bash
python scripts/verify_original_exports.py /path/to/EV_Final_Experiment_Exports.zip
```

This checks archive identities and the original saved model/state checksums without loading checkpoints or retraining. See [publishing instructions](docs/PUBLISHING.md).

## Historical results and license

Historical CSV summaries and notebooks are preserved from the supplied repository. Historical verification scripts recompute/check saved outputs; they do not reconstruct every original E1–E8 checkpoint or constitute a new full training replication. See [provenance](docs/PROVENANCE.md).

Repository code retains the MIT license. The KIT dataset remains subject to its publisher's terms. Funding: none. The author reports no competing interests. AI assistance and the distinction between source assistance and executable measurements are described in the article and [provenance notes](docs/PROVENANCE.md).
