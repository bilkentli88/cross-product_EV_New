"""Verify every packaged principal fit against its original saved state metrics.

Does not regenerate raw engineering features or load/train any model.
"""
from pathlib import Path
import hashlib
import itertools
import json

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
METRICS = ['hits1', 'hits3', 'mrr']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = {}
    for study, fit_count, state_count in [('e9', 150, 34065), ('e10', 300, 68130), ('e11', 210, 47691)]:
        source = ROOT / 'results/principal' / study
        protocol = json.loads((source / 'protocol.json').read_text())
        signature = hashlib.sha256(json.dumps(protocol, sort_keys=True).encode()).hexdigest()
        records = sorted((source / 'fits').glob('*.json'))
        table = pd.read_csv(source / (study + '_fit_results.csv')).set_index(['battery_id', 'seed', 'condition'])
        expected_keys = set(itertools.product(protocol['folds'], protocol['seeds'], protocol['conditions']))
        assert len(records) == len(table) == fit_count
        assert set(table.index) == expected_keys
        seen = set()
        rows = 0
        reused = 0
        for path in records:
            record = json.loads(path.read_text())
            key = record['battery_id'], record['seed'], record['condition']
            assert key in expected_keys and key not in seen
            seen.add(key)
            assert record['protocol_signature'] == signature
            state = path.with_name(path.stem + '_states.csv.gz')
            if 'states_sha256' in record:
                assert sha(state) == record['states_sha256'], state
            frame = pd.read_csv(state)
            n = record['n_states']
            assert len(frame) == n
            np.testing.assert_array_equal(frame.position.to_numpy(), np.arange(n))
            np.testing.assert_array_equal(frame.candidate_size.to_numpy(), np.arange(n, 0, -1))
            assert (frame.battery_id == key[0]).all() and (frame.seed == key[1]).all()
            assert (frame.condition == key[2]).all()
            values = frame[METRICS].to_numpy()
            assert np.isfinite(values).all() and ((values >= 0) & (values <= 1)).all()
            np.testing.assert_allclose(values.mean(axis=0), [record[m] for m in METRICS], rtol=0, atol=2e-12)
            np.testing.assert_allclose(values.mean(axis=0), table.loc[key, METRICS].astype(float).to_numpy(), rtol=0, atol=2e-12)
            np.testing.assert_allclose(frame[METRICS].iloc[-1].to_numpy(), 1, rtol=0, atol=1e-12)
            curve = record.get('loss_curve', [])
            if curve:
                assert len(curve) == 30 and all(np.isfinite(x['loss']) for x in curve)
            if study == 'e10' and record.get('origin', '').startswith('Verified E9 anchor'):
                reused += 1
                provenance = record['e9_provenance']
                old = f'battery{key[0]:02d}_seed{key[1]}_{provenance["original_condition"]}'
                original = ROOT / 'results/principal/e9/fits' / (old + '.json')
                assert sha(original) == provenance['record_sha256']
                assert sha(original.with_name(old + '_states.csv.gz')) == provenance['states_sha256']
                original_record = json.loads(original.read_text())
                np.testing.assert_allclose([record[m] for m in METRICS], [original_record[m] for m in METRICS], rtol=0, atol=2e-12)
            rows += n
        assert seen == expected_keys and rows == state_count
        if study == 'e10':
            assert reused == 120
        report[study] = {'fit_records': fit_count, 'state_rows': rows, 'e9_reused_endpoints': reused}
    report['status'] = 'PASS: all 660 saved fit/state records; no feature regeneration or model fitting'
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
