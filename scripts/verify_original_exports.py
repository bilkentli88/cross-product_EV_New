"""Validate the separate companion ZIP containing unchanged original exports.

Usage: python scripts/verify_original_exports.py EV_Final_Experiment_Exports.zip
No checkpoint deserialization, dataset access or training occurs.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import zipfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
METRICS = ['hits1', 'hits3', 'mrr']


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exports', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'provenance/source_archives.json').read_text())
    report = {}
    e9_source = None
    with zipfile.ZipFile(args.exports) as outer:
        assert outer.testzip() is None
        for info in manifest:
            payload = outer.read('raw_exports/' + info['file_name'])
            assert len(payload) == info['size_bytes'] and digest(payload) == info['sha256']
            archive = zipfile.ZipFile(io.BytesIO(payload))
            assert archive.testzip() is None
            if info['study'] == 'e9':
                e9_source = archive
            records = sorted(n for n in archive.namelist() if n.startswith('fits/') and n.endswith('.json'))
            checked_models = 0
            checked_states = 0
            reused = 0
            for name in records:
                record = json.loads(archive.read(name))
                stem = name.removesuffix('.json')
                state_payload = archive.read(stem + '_states.csv.gz')
                if 'states_sha256' in record:
                    assert digest(state_payload) == record['states_sha256']
                frame = pd.read_csv(io.BytesIO(state_payload), compression='gzip')
                assert len(frame) == record['n_states']
                np.testing.assert_allclose(frame[METRICS].mean().to_numpy(), [record[m] for m in METRICS], rtol=0, atol=2e-12)
                checked_states += 1
                extension = '.ubj' if record['condition'].endswith('XGB') else '.pt'
                model_name = 'models/' + Path(stem).name + extension
                model_payload = archive.read(model_name)
                if 'model_sha256' in record:
                    assert digest(model_payload) == record['model_sha256']
                    checked_models += 1
                if info['study'] == 'e10' and record.get('e9_provenance'):
                    provenance = record['e9_provenance']
                    key = f'battery{record["battery_id"]:02d}_seed{record["seed"]}_{provenance["original_condition"]}'
                    assert digest(e9_source.read('fits/' + key + '.json')) == provenance['record_sha256']
                    assert digest(e9_source.read('fits/' + key + '_states.csv.gz')) == provenance['states_sha256']
                    assert digest(e9_source.read('models/' + key + extension)) == provenance['model_sha256']
                    reused += 1
            if info['study'] == 'e10':
                assert reused == 120 and len(records) == 300
            elif info['study'] == 'e9':
                assert len(records) == 150
            elif info['study'] == 'e11':
                assert len(records) == 210
            report[info['study']] = {'source_sha256_verified': True, 'fit_means': checked_states,
                                      'model_checksums_in_fit_records_verified': checked_models,
                                      'e9_reuse_provenance_verified': reused}
    print(json.dumps({'status': 'PASS', 'exports': report,
                      'scope': 'Original archive hashes/CRC, fit means and available model/state hashes; models not loaded'}, indent=2))


if __name__ == '__main__':
    main()
