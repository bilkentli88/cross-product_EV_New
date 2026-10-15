"""Print compact manuscript-facing summaries from saved extended results.

This script does not retrain models. It verifies that the extended result files
needed for the manuscript are present and prints the aggregate values and the
central product-level contrasts used in the paper.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
EXT = ROOT / "results" / "historical" / "extended"


def read_csv(relative):
    path = EXT / relative
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def show(title, df, columns=None):
    print(f"\n{title}")
    if columns is not None:
        df = df[columns]
    print(df.to_string(index=False))


def main():
    e1_agg = read_csv("e1_test_time_swap/test_time_topology_swap_aggregate.csv")
    e1_ctr = read_csv("e1_test_time_swap/test_time_topology_swap_contrasts.csv")
    show("E1 aggregate", e1_agg)
    show(
        "E1 designated Hits@1 contrasts",
        e1_ctr[e1_ctr["metric"] == "hits1"],
        ["contrast_id", "contrast", "mean_difference", "p_exact", "p_holm_hits1"],
    )

    e2_agg = read_csv("e2_global_context/e2_aggregate.csv")
    show(
        "E2 aggregate",
        e2_agg,
        ["condition_summary", "hits1", "hits3", "mrr"],
    )

    e2b = read_csv("e2b_capacity_matched_meanpool/e2b_aggregate.csv")
    show("E2b capacity-matched mean-pool", e2b)

    e3 = read_csv("e3_strong_baselines/e3_aggregate.csv")
    show("E3 baselines", e3, ["method", "hits1", "hits3", "mrr"])

    e4 = read_csv("e4_training_budget/e4_aggregate.csv")
    show(
        "E4 training-budget aggregate",
        e4,
        ["epoch", "condition_summary", "hits1", "hits3", "mrr"],
    )

    e5_agg = read_csv("e5_positive_control/e5_aggregate.csv")
    e5_ctr = read_csv("e5_positive_control/e5_contrasts.csv")
    show("E5 positive-control aggregate", e5_agg)
    show(
        "E5 designated Hits@1 contrasts",
        e5_ctr[(e5_ctr["metric"] == "hits1") & (e5_ctr["primary_hits1_family"] == True)],
        ["contrast", "mean_difference", "positive_products", "p_exact", "p_holm_primary_hits1"],
    )

    e6_agg = read_csv("e6_state_aware/e6_aggregate.csv")
    e6_ctr = read_csv("e6_state_aware/e6_contrasts.csv")
    show("E6 state-aware aggregate", e6_agg)
    show(
        "E6 designated Hits@1 contrasts",
        e6_ctr[(e6_ctr["metric"] == "hits1") & (e6_ctr["primary_hits1_family"] == True)],
        [
            "contrast",
            "mean_difference",
            "ci_low",
            "ci_high",
            "positive_products",
            "p_exact",
            "p_holm_primary_hits1",
        ],
    )

    e8_agg = read_csv("e8_manufacturer_exclusion/e8_aggregate.csv")
    e8_ctr = read_csv("e8_manufacturer_exclusion/e8_contrast.csv")
    show("E8 manufacturer-exclusion aggregate", e8_agg)
    show("E8 contrasts", e8_ctr)

    print("\nExtended result-file check completed successfully.")


if __name__ == "__main__":
    main()
