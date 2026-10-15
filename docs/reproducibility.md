# Reproducing the principal audit

Run commands from the repository root with Python 3.10 or newer. The notebooks were designed for Colab and contain normal Colab Drive authorization. The saved-output verification commands do not use Drive or network access.

## 1. Verify saved results first

Install `requirements.txt`, then run `scripts/verify_repository.py`, `scripts/verify_saved_statistics.py`, `scripts/verify_state_records.py`, and `scripts/regenerate_figures.py`. The first three scripts are read-only and fail on inconsistent records. Figures go into `generated_figures/` by default; override with `--output-dir PATH`.

- E9: 150 fit/state records, five conditions, ten products, three seeds.
- E10: 300 records; 120 verified endpoint reuses and 180 new fits. Reused endpoints are not independent replications.
- E11: 210 new fits; 30 Real, 150 ActiveShuffle, 30 NoEdge. The matched E11 Real reference is separate from E9's GNN.

`verify_saved_statistics.py` recomputes all fit-to-product-to-aggregate means, the 12 designated Hits@1 exact sign-flip tests, their three separate Holm families, and the stored descriptive intervals. `verify_state_records.py` additionally reconstructs each fit mean from its saved per-state ranking metrics, validates product/seed/condition identifiers, positions, candidate sizes, metric bounds, protocol signatures and available state checksums, and checks E10's reused endpoint provenance against E9. This does not regenerate features from raw engineering data or re-evaluate neural checkpoints.

## 2. Data and full retraining

The raw dataset is external; see `data/README.md`. Open the self-contained notebooks in Colab and run their numbered cells in order. All folds must have matching original CSV hashes. Raw identifiers are lookup keys, not model features; future order provides targets, not predictive input. Keep the post-current-operation updater, full candidate evaluation and training-only categorical vocabularies unchanged.

1. **E9:** open `notebooks/E9_State_Aware_Baselines.ipynb`. Set `DATA_PATH` to the CSV directory or KIT archive if needed. With the default scientific settings the full study has 150 fits. Output is saved after each completed fit.
2. **E10:** open `notebooks/E10_State_Feature_Families.ipynb`. For the recorded reuse path, supply the original E9 archive or extracted directory in `E9_RESULTS_PATH` and keep `REUSE_E9_ANCHORS=True`. The preflight verifies all eligible anchors; all 120 passed in the reported run. Enable full training in its Cell 11 to train the 180 new intermediates. To run without supplied anchors, set `REUSE_E9_ANCHORS=False`; all 300 records are then newly trained and are a new replication, not the recorded reuse provenance.
3. **E11:** open `notebooks/E11_Canonical_Degree_Adjacency.ipynb`. Its reported E9 reuse gate failed, so all 210 fits were new. For a fresh full replication without anchor inputs, set `REUSE_E9_REAL=False`; otherwise supply the original E9 export and let the gate decide. The default Step 7 launches full training after preflight.

E9 and E11 default `RUN_FULL_EXPERIMENT=True`; E10 defaults to `False` in its full-run cell. Use the CSV verification scripts for inspection without training. The delivered notebooks are preserved byte for byte so saved source hashes remain meaningful. Their early preparation/interpretation prose is historical context, not an assertion that the completed exports are missing.

For local notebook execution, disable Colab-only Drive behavior where necessary, set `DATA_PATH` and output paths explicitly, and run cells in order. No guarantee of a successful unchanged end-to-end local training run is made by this packaging check. Do not bypass reuse-gate failures to manufacture identical endpoints. Separate dependency/device signatures create separate run directories.

## 3. Original exports and E10 provenance

The companion `EV_Final_Experiment_Exports.zip` contains nested archives listed in `provenance/source_archives.json`. Extract the E9 nested ZIP before pointing a notebook to it; alternatively extract it to a directory containing its `protocol.json`, `fits`, `models`, and `diagnostics`.

The original E10 archive contains 300 fit/state/model records and diagnostics but did not contain its final summary/completion files. Those were independently reconstructed and are retained as a separate `e10_verified_summaries.zip`. The repository combines their nonconflicting files for convenient inspection, and `results/principal/e10/provenance/` retains both source README files. The original archives are never silently rewritten.

Run `python scripts/verify_original_exports.py PATH_TO_COMPANION_ZIP` to verify all source archive SHA-256 values, archive CRC integrity, per-fit metrics and available checkpoint/state hashes. Saved model files are never deserialized by this verification script. E9 did not export per-fit model checksums; its original archive hash and the packaged-file manifest establish byte identity, while E10 reused anchors carry additional E9 model/state provenance hashes.

## 4. Numerical and statistical interpretation

Average seeds and five shuffle realizations within product; then weight the ten products equally. Exact two-sided sign-flip inference enumerates 1024 product-sign assignments under a sign-exchangeability assumption. Holm correction is separate for E9's four, E10's six, and E11's two Hits@1 contrasts. Descriptive bootstrap intervals use 10000 product resamples and seed 20261003. Supporting metrics, singleton removal, progress stages and omissions are descriptive. This is not whole-study family-wise correction or proof of independent products under overlapping LOPO training folds.

The retained CPU sensitivity re-evaluated all 210 E11 checkpoints previously. It changes 376 of 143073 metric cells and preserves both principal sign-flip/Holm conclusions. Packaging verifies the retained numerical records; it does not repeat that checkpoint evaluation. Original GPU outputs remain primary. Per-state ranking metrics are included; original per-candidate GPU score vectors were not exported, so a near-tie device explanation remains an inference.

## 5. Historical supporting material

Use `python scripts/historical/recompute_statistics.py`, `python scripts/historical/check_extended_results.py`, and `python scripts/historical/check_stateaware_xgb.py` for older saved outputs. Their paths were adapted to `results/historical/`; their numerical logic was preserved. The historical XGB-only notebook labelled E9 maps to Supplementary S11.1 and must not be used as the principal E9 endpoint. Historical E6 shuffling jointly changes degree/state-event correspondence; it is not E11's canonical-degree-conditioned control.
