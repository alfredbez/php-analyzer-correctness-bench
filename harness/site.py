#!/usr/bin/env python3
"""Render one offline-capable, private HTML review surface from measured JSON."""

import argparse
import json
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / 'web'


def render(payload: dict) -> str:
    if payload.get('schema_version') != 1 or not payload.get('profiles') or 'cases' not in payload:
        raise ValueError('expected a version-1 measured comparison with case evidence')
    template = (ASSETS / 'report.html').read_text()
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c')
    return (template.replace('/* REPORT_CSS */', (ASSETS / 'report.css').read_text())
            .replace('/* REPORT_JS */', (ASSETS / 'report.js').read_text())
            .replace('REPORT_DATA', serialized))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--comparison', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.comparison).read_text())
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render(payload))
    print(destination)


if __name__ == '__main__':
    main()
