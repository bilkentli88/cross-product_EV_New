"""Check file provenance, notebook JSON structure/Python syntax and local links.

Does not execute notebook cells. This is not nbformat schema validation.
"""
from pathlib import Path
import ast
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'provenance/file_manifest.json').read_text())
    for record in manifest:
        path = ROOT / record['path']
        assert path.is_file(), path
        assert path.stat().st_size == record['size_bytes'], path
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], path
    notebooks = 0
    cells = 0
    for path in sorted((ROOT / 'notebooks').rglob('*.ipynb')):
        document = json.loads(path.read_text())
        assert document['nbformat'] == 4 and isinstance(document['cells'], list)
        assert isinstance(document['metadata'], dict)
        for index, cell in enumerate(document['cells']):
            assert cell['cell_type'] in {'code', 'markdown', 'raw'}
            assert isinstance(cell['metadata'], dict)
            assert isinstance(cell['source'], (list, str))
            if cell['cell_type'] == 'code':
                assert isinstance(cell['outputs'], list)
                assert cell['execution_count'] is None or isinstance(cell['execution_count'], int)
                text = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])
                ast.parse(text, filename=f'{path.relative_to(ROOT)} cell {index}')
                cells += 1
            else:
                assert 'outputs' not in cell and 'execution_count' not in cell
        notebooks += 1
    for path in (ROOT / 'scripts').rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
    sources = json.loads((ROOT / 'provenance/principal_notebooks.json').read_text())
    for record in sources:
        path = ROOT / record['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256']
        document = json.loads(path.read_text())
        code = [c['source'] for c in document['cells'] if c['cell_type'] == 'code']
        assert hashlib.sha256(json.dumps(code, ensure_ascii=False).encode()).hexdigest() == record['code_cells_sha256']
    # Current entry-point documentation uses resolvable local Markdown links.
    for name in ['README.md', 'docs/reproducibility.md', 'docs/PROVENANCE.md', 'docs/PUBLISHING.md']:
        path = ROOT / name
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in target and not target.startswith('#'):
                assert (path.parent / target.split('#', 1)[0]).exists(), (path, target)
    print(json.dumps({'status': 'PASS', 'manifest_files': len(manifest), 'notebooks': notebooks,
                      'python_code_cells_syntax_checked': cells,
                      'principal_notebooks_preserved_byte_for_byte': len(sources),
                      'scope': 'Integrity, notebook structural checks and Python syntax; no notebook execution or full nbformat schema check'}, indent=2))


if __name__ == '__main__':
    main()
