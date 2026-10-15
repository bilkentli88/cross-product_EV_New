E9 state-aware non-graph baseline experiment

Read e9_completion.json before interpreting the results. e9_fit_results.csv holds
seed-level results; e9_fold_mean.csv averages seeds within product; e9_aggregate.csv
averages products equally. e9_contrasts.csv uses the four planned Hits@1 comparisons
with Holm correction. Hits@3/MRR, stage analyses, and singleton sensitivities are
supporting/descriptive. Product bootstrap intervals are descriptive. Exact sign-flip
enumeration relies on the product-level sign-exchangeability null assumption;
overlapping LOPO training sets and the small product collection limit population claims.

StaticFeature controls and StateAware controls have matched architecture/features;
only state summaries change. Shared-component indicators are present in both.
Non-graph does not mean no engineering-derived features: local fixation counts,
type histograms, and activity/completion flags are derived from the E6 state.
These learners receive no adjacency or message passing. DynamicReal is the original
E6 implementation rerun in this notebook. The old E6 CSV is historical context only.

No test-product hyperparameter selection, IDs, candidate positions, or future target
pointers enter model inputs. Prefix operations update state; candidates are inventory
minus executed operations and randomly ordered at evaluation. Fixed/no-operation
connections keep the original E6 handling, even if completed nodes remain active.

The raw dataset is external: DOI 10.35097/emz24pksshndq468. CSV hashes, source notebook
hash, dependency versions, feature names, vocabulary and parameter counts are saved.
