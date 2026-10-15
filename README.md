# Physical Topology and Process State in Cross-Product EV Battery Disassembly Ranking

Code, experiment configurations, saved results, and verification scripts accompanying **Physical Topology and Process State in Cross-Product EV Battery Disassembly Ranking: A Controlled Representation Audit**.

The study evaluates next-operation ranking across ten EV battery products using leave-one-product-out evaluation. It compares state-aware non-graph learners, feature-update controls, and graph-adjacency controls. Evaluation uses the recorded operation prefix and an unordered inventory of remaining operations; the target is the recorded successor. The reported metrics measure reference-operation ranking rather than physical feasibility or planning success.

## Verify the reported results

Run these commands from the repository root with Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
python scripts/verify_repository.py
python scripts/verify_saved_statistics.py
python scripts/verify_state_records.py
python scripts/regenerate_figures.py
```

| Command | Purpose |
|---|---|
| `verify_repository.py` | Check file hashes, notebook structure, Python syntax, and documentation links. |
| `verify_saved_statistics.py` | Recompute product-level aggregates, designated exact sign-flip tests, Holm-adjusted p-values, and descriptive bootstrap intervals. |
| `verify_state_records.py` | Reconstruct all 660 fit-record means from saved per-state metrics and check identifiers, protocol signatures, available checksums, and reused-record provenance. |
| `regenerate_figures.py` | Regenerate the two result plots in `generated_figures/`. |

This workflow requires no raw dataset, GPU, or model training. It verifies the supplied numerical records; it does not regenerate raw-data features or re-evaluate model checkpoints. See the [validation report](docs/VALIDATION_REPORT.md) for the verification scope.

## Analyses and source files

| Analysis | Notebook | Saved results |
|---|---|---|
| State-aware MLP and XGBoost baselines, initial-state controls, and matched GNN comparison | [State-aware baselines](notebooks/E9_State_Aware_Baselines.ipynb) | [Baseline records](results/principal/e9/) |
| Controlled updates of global, status, and structural feature families | [Feature-family controls](notebooks/E10_State_Feature_Families.ipynb) | [Feature-family records](results/principal/e10/) |
| Real, active-shuffled, and no-edge adjacency with retained physical-degree and semantic inputs | [Adjacency controls](notebooks/E11_Canonical_Degree_Adjacency.ipynb) | [Adjacency records](results/principal/e11/) |

Experiment identifiers in filenames provide stable links between notebooks, protocols, and exported records. The baseline comparison and adjacency control use separately trained GNN references; use the reference scores from the corresponding analysis.

The collections contain 150 baseline records, 300 feature-family records, and 210 adjacency-control records. The feature-family collection includes 120 verified baseline endpoints and 180 newly trained fits; reused endpoints are not independent replications. The adjacency collection contains 30 real-adjacency, 150 shuffled-adjacency, and 30 no-edge fits.

## Dataset and model training

Obtain the EV battery disassembly dataset from Karlsruhe Institute of Technology:

**<https://doi.org/10.35097/emz24pksshndq468>**

The dataset is distributed by its publisher and is not included here. [Dataset instructions](data/README.md) identify the four required CSV files and their SHA-256 hashes.

The notebooks support Google Colab. Run their numbered cells in order and set the dataset and output paths. A GPU is recommended for neural training.

- The baseline notebook enables full training by default.
- The feature-family notebook requires enabling its full-run cell. Its reference-reuse mode requires the baseline export; a fresh-training mode is also documented.
- The adjacency notebook enables full training by default and supports fresh training without supplied reference checkpoints.

For Colab, use the notebook setup cells. For local execution, install `requirements-training.txt` and adapt Colab-specific Drive mounting and paths. Follow the [detailed reproduction instructions](docs/reproducibility.md) for the analysis-specific settings.

[Recorded software environments](configs/recorded_environments.json) list the package versions captured in the reported runs. Training requirements provide dependency ranges rather than an exact environment lock; numerical outputs may vary with software and hardware. Saved protocols in each results directory specify the corresponding experimental settings.

## Evaluation and statistical analysis

Neural-training seeds are 17, 29, and 43. Results are averaged across training seeds and, where applicable, five shuffle realizations within each product, then averaged with equal weight across the ten held-out products.

The designated Hits@1 comparisons use exact two-sided product-level sign-flip tests over all 1,024 sign assignments. Holm correction is applied separately to the four baseline, six feature-family, and two adjacency comparisons. Descriptive bootstrap intervals use 10,000 product resamples with seed 20261003. Protocol files and the [reproduction instructions](docs/reproducibility.md) specify randomization settings, comparisons, and interpretation limits, including overlapping training folds and the sign-exchangeability assumption.

## Checkpoints and original exports

The source tree contains protocols, fit summaries, per-state ranking metrics, diagnostics, and analysis scripts. Model weights are supplied separately in the companion **`EV_Final_Experiment_Exports.zip`**, containing the original experiment exports and verified feature-family summaries. See [Releases](https://github.com/bilkentli88/cross-product_EV_New/releases) for published download assets.

After obtaining the companion archive, verify it with:

```bash
python scripts/verify_original_exports.py /path/to/EV_Final_Experiment_Exports.zip
```

This checks archive identities, integrity, and available saved model/state checksums without loading model weights. Archive hashes are recorded in [the source manifest](provenance/source_archives.json). Original exports contain per-state ranking metrics; per-candidate GPU score vectors were not exported.

## Repository guide

| Location | Contents |
|---|---|
| `notebooks/` | Notebooks for the three principal analyses. |
| `results/principal/` | Protocols, fit records, per-state metrics, diagnostics, and aggregate results. |
| `results/audits/` | Numerical checks and CPU sensitivity records. |
| `configs/` | Protocol summary and recorded software environments. |
| `scripts/` | Integrity checks, statistical verification, and figure generation. |
| `provenance/` | Source hashes and file-integrity records. |
| `figures/published/` | Supplied result figures. |
| `data/` | Dataset retrieval and integrity instructions. |
| `docs/` | Detailed reproduction instructions and validation documentation. |

Additional supporting notebooks, results, and scripts are retained in the `historical/` subdirectories. Their relationship to the principal analyses and supplementary results is documented in the [provenance guide](docs/PROVENANCE.md).

## Citation and license

Repository citation metadata are provided in [CITATION.cff](CITATION.cff). Code is distributed under the [MIT license](LICENSE). The external dataset remains subject to its publisher's terms.
