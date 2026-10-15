# Uploading the cleaned repository

1. Extract `cross-product_EV_New_clean.zip`. Upload the **contents of its single repository folder** to the repository root; do not upload an extra nested project folder or just the ZIP as the entire repository.
2. Remove superseded root paths from the old repository after keeping a local backup: the old `notebooks` and `results` contents now belong under their explicit `historical` subfolders. Simply overlaying the ZIP without deleting superseded files leaves ambiguous duplicate E9 protocols. The new root README and `configs/principal_experiment_config.json` replace the old narrative and default settings.
3. Run the quick verification commands in the README from a fresh extracted copy. They do not retrain models.
4. Create a GitHub Release for this manuscript snapshot and attach the separate `EV_Final_Experiment_Exports.zip` as a release asset. Copy its actual published download URL into the release description and the README's Original exports section. The asset includes unchanged checkpoints and original exports and is intentionally outside the source ZIP.
5. Check the repository and release link while signed out. Only then describe the uploaded contents as publicly available in the manuscript. Update the bibliography entry to `https://github.com/bilkentli88/cross-product_EV_New`; `docs/code_data_availability.tex` contains the identified-manuscript wording and `docs/GraphEVRepo.bib` provides the repository citation.

This package does not push, commit or publish anything to GitHub. The named repository identifies the author; use an anonymous code archive/link for the journal's anonymized review files as required.
