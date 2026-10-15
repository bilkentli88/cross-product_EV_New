"""Recompute saved fit/product aggregates, contrast intervals and primary tests.

No dataset, checkpoint loading, GPU or retraining is used.
"""
from pathlib import Path
import itertools
import json

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
METRICS = ['hits1', 'hits3', 'mrr']
SEEDS = {17, 29, 43}
SIGNS = np.array(list(itertools.product([-1.0, 1.0], repeat=10)))


def exact_signflip(d):
    return float(np.mean(np.abs(SIGNS @ d / len(d)) >= abs(d.mean()) - 1e-12))


def holm(pvalues):
    values = np.asarray(pvalues, dtype=float)
    order = np.argsort(values, kind='stable')
    adjusted = np.empty_like(values)
    adjusted[order] = np.minimum(1, np.maximum.accumulate(values[order] * (len(values) - np.arange(len(values)))))
    return adjusted


def main():
    report = {}
    for study, key, expected_fits, expected_tests in [
        ('e9', 'condition', 150, 4), ('e10', 'condition', 300, 6), ('e11', 'family', 210, 2)
    ]:
        source = ROOT / 'results/principal' / study
        fits = pd.read_csv(source / (study + '_fit_results.csv'))
        product = pd.read_csv(source / (study + '_fold_mean.csv'))
        aggregate = pd.read_csv(source / (study + '_aggregate.csv')).set_index(key)
        contrasts = pd.read_csv(source / (study + '_contrasts.csv'))
        assert len(fits) == expected_fits and set(fits.seed) == SEEDS
        assert set(fits.battery_id) == set(range(1, 11))
        assert not fits.duplicated(['battery_id', 'seed', 'condition']).any()
        actual = fits.groupby(['battery_id', key])[METRICS].mean().sort_index()
        expected = product.set_index(['battery_id', key])[METRICS].sort_index()
        assert actual.index.equals(expected.index)
        np.testing.assert_allclose(actual.to_numpy(), expected.to_numpy(), rtol=0, atol=2e-12)
        computed = product.groupby(key)[METRICS].mean().sort_index()
        np.testing.assert_allclose(computed.to_numpy(), aggregate.loc[computed.index, METRICS].to_numpy(), rtol=0, atol=2e-12)

        exact_primary = []
        primary = contrasts[contrasts.metric == 'hits1']
        assert len(primary) == expected_tests
        for _, row in contrasts.iterrows():
            a, b = row.contrast.split(' - ')
            values = product.pivot(index='battery_id', columns=key, values=row.metric).sort_index()
            d = (values[a] - values[b]).to_numpy()
            rng = np.random.default_rng(20261003)
            draws = rng.choice(d, (10000, len(d)), replace=True).mean(axis=1)
            low, high = np.quantile(draws, [0.025, 0.975])
            p = exact_signflip(d)
            np.testing.assert_allclose([d.mean(), low, high, p],
                                       [row.mean_difference, row.bootstrap95_low, row.bootstrap95_high, row.p_exact],
                                       rtol=0, atol=2e-12)
            wins = row.get('wins', row.get('product_wins'))
            assert int((d > 0).sum()) == int(wins)
            if row.metric == 'hits1':
                exact_primary.append(p)
        adjusted = holm(exact_primary)
        np.testing.assert_allclose(adjusted, primary.p_holm.to_numpy(), rtol=0, atol=2e-12)
        report[study] = {'fits': len(fits), 'products': 10, 'primary_tests': len(primary),
                         'all_contrast_intervals_checked': len(contrasts), 'p_holm': adjusted.tolist()}

    f10 = pd.read_csv(ROOT / 'results/principal/e10/e10_fit_results.csv')
    f11 = pd.read_csv(ROOT / 'results/principal/e11/e11_fit_results.csv')
    assert f10.origin.str.startswith('Verified E9 anchor').sum() == 120
    assert f10.origin.str.startswith('New E10').sum() == 180
    assert f11.origin.eq('New E11 training').all()
    a9 = pd.read_csv(ROOT / 'results/principal/e9/e9_aggregate.csv').set_index('condition')
    a10 = pd.read_csv(ROOT / 'results/principal/e10/e10_aggregate.csv').set_index('condition')
    for learner in ['MLP', 'XGB']:
        for dest, source in [('Full', 'StateAware'), ('Static', 'StaticFeature')]:
            np.testing.assert_allclose(a10.loc[dest + learner, METRICS].astype(float),
                                       a9.loc[source + learner, METRICS].astype(float), rtol=0, atol=2e-12)

    # Verify the retained CPU diagnostic from its 210 saved per-fit deltas.
    cpu = pd.read_csv(ROOT / 'results/audits/cpu_reevaluation_all_fits.csv')
    merged = f11.merge(cpu, on=['battery_id', 'seed', 'condition', 'n_states'], validate='one_to_one')
    assert len(merged) == 210 and int(cpu.different_metric_cells.sum()) == 376
    for metric in METRICS:
        merged[metric] += merged['mean_delta_' + metric]
    cp = merged.groupby(['battery_id', 'family'])[METRICS].mean().reset_index()
    ca = cp.groupby('family')[METRICS].mean().sort_index()
    saved_ca = pd.read_csv(ROOT / 'results/audits/cpu_sensitivity_aggregate.csv').set_index('family').sort_index()
    np.testing.assert_allclose(ca.to_numpy(), saved_ca[METRICS].to_numpy(), rtol=0, atol=2e-12)
    saved_cc = pd.read_csv(ROOT / 'results/audits/cpu_sensitivity_contrasts.csv')
    pivot = cp.pivot(index='battery_id', columns='family', values='hits1').sort_index()
    ps = []
    for _, row in saved_cc.iterrows():
        a, b = row.contrast.split(' - ')
        delta = (pivot[a] - pivot[b]).to_numpy()
        ps.append(exact_signflip(delta))
        np.testing.assert_allclose([delta.mean(), ps[-1]], [row.mean_difference, row.p_exact], rtol=0, atol=2e-12)
    np.testing.assert_allclose(holm(ps), saved_cc.p_holm.to_numpy(), rtol=0, atol=2e-12)
    report['provenance_and_retained_cpu_diagnostic'] = 'passed; no checkpoint reevaluation performed'
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
