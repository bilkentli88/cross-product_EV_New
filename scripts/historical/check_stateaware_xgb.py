"""Audit saved StateAwareXGBRanker results, without rerunning model fits.

Usage: python scripts/check_stateaware_xgb.py

Requires NumPy and pandas. Loads canonical GPU-run E9 results and independent E6
DynamicReal per-product results. Treats held-out product (n=10) as the unit.
This DOES NOT validate feature construction or the correctness of source data.
"""
import itertools
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
E9 = ROOT / "results/historical/extended/e9_stateaware_xgb"
E6 = ROOT / "results/historical/extended/e6_state_aware"


def exact_signflip(d):
    d = np.asarray(d, dtype=float)
    observed = abs(d.mean())
    means = [abs(np.mean(d * signs))
             for signs in itertools.product((-1.0, 1.0), repeat=len(d))]
    return float(np.mean(np.asarray(means) >= observed - 1e-12))


def bootstrap_ci(d):
    rng = np.random.default_rng(20261011)
    d = np.asarray(d, dtype=float)
    ids = rng.integers(0, len(d), size=(20000, len(d)))
    return np.percentile(d[ids].mean(axis=1), [2.5, 97.5])


def main():
    seed = pd.read_csv(E9 / "stateaware_xgb_seed_results.csv")
    fold = pd.read_csv(E9 / "stateaware_xgb_fold_mean.csv")
    agg = pd.read_csv(E9 / "stateaware_xgb_aggregate.csv")
    stored_products = pd.read_csv(E9 / "stateaware_xgb_vs_dynamicreal_products.csv")
    stored_contrast = pd.read_csv(E9 / "stateaware_xgb_vs_dynamicreal_contrast.csv")
    e6 = pd.read_csv(E6 / "e6_fold_mean.csv")
    assert len(seed) == 30 and len(fold) == 10, (len(seed), len(fold))
    assert seed["battery_id"].nunique() == 10 and seed["seed"].nunique() == 3
    assert not seed.duplicated(["battery_id", "seed"]).any()
    for key in ["hits1", "hits3", "mrr"]:
        from_seed = seed.groupby("battery_id")[key].mean().sort_index()
        from_fold = fold.set_index("battery_id")[key].sort_index()
        np.testing.assert_allclose(from_seed, from_fold, rtol=0, atol=1e-10)
        np.testing.assert_allclose(from_fold.mean(), agg[key].iloc[0], rtol=0, atol=1e-10)

    e6 = e6[e6["condition_summary"] == "dynamic_real"]
    assert len(e6) == 10
    paired = e6[["battery_id", "hits1", "hits3", "mrr"]].merge(
        fold[["battery_id", "hits1", "hits3", "mrr"]],
        on="battery_id", validate="one_to_one", suffixes=("_dynamic_real", "_stateaware_xgb"))
    paired = paired.sort_values("battery_id")
    stored = stored_products.sort_values("battery_id")
    assert len(paired) == len(stored) == 10
    for key in ["hits1", "hits3", "mrr"]:
        d = paired[f"{key}_dynamic_real"] - paired[f"{key}_stateaware_xgb"]
        np.testing.assert_allclose(d.to_numpy(), stored[f"difference_{key}"].to_numpy(),
                                   rtol=0, atol=1e-10)
    d = (paired["hits1_dynamic_real"] - paired["hits1_stateaware_xgb"]).to_numpy()
    p = exact_signflip(d)
    ci = bootstrap_ci(d)
    row = stored_contrast.iloc[0]
    assert np.isclose(d.mean(), row["mean_difference"], atol=1e-12)
    assert np.isclose(p, row["p_exact_two_sided"], atol=1e-12)
    np.testing.assert_allclose(ci, [row["descriptive_ci_low"], row["descriptive_ci_high"]], rtol=0, atol=1e-8)
    assert (d > 0).sum() == int(row["positive_products"]) and (d < 0).sum() == int(row["negative_products"])
    print("PASS: 30 seed fits, 10 products, aggregates, E6 matching and exact sign-flip comparison")
    print(f"StateAwareXGBRanker Hits@1={agg.hits1.iloc[0]:.6f}, Hits@3={agg.hits3.iloc[0]:.6f}, MRR={agg.mrr.iloc[0]:.6f}")
    print(f"DynamicReal minus StateAwareXGBRanker Hits@1={d.mean():+.6f}; p={p:.9f}; descriptive 95% CI={ci}")
    print("IMPORTANT: This verifies SAVED OUTPUTS ONLY; no retraining or dataset-level audit performed.")


if __name__ == "__main__":
    main()
