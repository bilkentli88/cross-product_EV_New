# Package validation report

Validation performed for this cleanup on 15 October 2026. Saved scientific measurements were not edited and full model training was not rerun.

| Check | Result |
|---|---|
| Principal notebook bytes | All 3 identical to the delivered final notebooks |
| Notebook JSON/basic structure and Python syntax | 17 notebooks; 323 code cells parse; no notebook cell execution |
| Principal fit-to-product-to-aggregate reconstruction | E9 150, E10 300, E11 210 records; passed |
| Product-paired contrast means and bootstrap intervals | All 36 saved metric contrasts reproduced |
| Designated exact sign-flip/Holm comparisons | 4 E9, 6 E10, 2 E11; passed |
| Original saved per-state metrics | 149886 state rows over all 660 records; fit means, identifiers, positions, candidate sizes, metric bounds and protocol signatures checked |
| E10 reused endpoints | 120 source record/state identities and metrics verified against E9 |
| E11 retained CPU diagnostic | All 210 saved per-fit deltas reconstruct the retained CPU means and primary tests; no checkpoint re-evaluation in this cleanup |
| Historical outputs/notebook preservation | 100 source files retain identical bytes at the corresponding historical paths |
| Historical canonical/no-progress statistics script | Passed |
| Historical extended-results file check | Passed; this command prints saved summaries and is not a new raw-data audit |
| Historical XGB-only comparator check | Passed; separate from the final E9 |
| Original export hashes and ZIP CRCs | All 4 unchanged source archives passed |
| Original checkpoint/state checksums | All available E10 (300) and E11 (210) model/state hash pairs matched; E9 archive hash checked because its fits did not export per-model hashes |
| Original export fit means | All 660 original records reproduce their saved per-state means |
| Figure regeneration | Both result figures generated successfully from packaged summary CSVs |
| Credential-pattern scan | No matching common access-token patterns found |

The packaged-file integrity and entry-point Markdown links are checked by `python scripts/verify_repository.py`; the file manifest covers the files shipped in this source snapshot. It does not cover later user-generated output directories.

## Practical boundaries

These checks inspect saved numerical records and code structure; they do not constitute full fresh model training, full nbformat JSON-schema validation, new all-product feature regeneration, hardware execution validation, or proof of physically feasible plans. The original external KIT dataset and the optional checkpoint bundle are required for deeper data/model re-evaluation. Historical original checkpoints are not reconstructed here. Exact GPU candidate score vectors were not exported.

The source repository ZIP and the companion export ZIP have separate purposes: upload source contents to GitHub, and attach the large original-export bundle as a GitHub Release asset if publishing checkpoint files.
