#!/usr/bin/env python3
"""Build the opt-in Pzoom experiment from an immutable source and dependency lock."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REF = 'c8162978033745e585f8e60d15a66a48862333cc'
URL = 'https://github.com/muglug/pzoom.git'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()
    source = ROOT / '.tools-alt/pzoom-source'
    if not source.exists():
        subprocess.run(['git', 'init', str(source)], check=True)
        subprocess.run(['git', '-C', str(source), 'fetch', '--depth', '1', URL, REF], check=True)
        subprocess.run(['git', '-C', str(source), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
    actual = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip()
    if actual != REF or dirty:
        raise RuntimeError('Pzoom source must be clean and match the pinned commit')
    lock = ROOT / 'tools/pzoom-Cargo.lock'
    shutil.copy2(lock, source / 'Cargo.lock')
    subprocess.run(['cargo', 'build', '--locked', '--release', '--bin', 'pzoom',
                    '-j', str(args.jobs)], cwd=source, check=True)
    binary = ROOT / 'tools/bin/pzoom'
    binary.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / 'target/release/pzoom', binary)
    shutil.copy2(source / 'LICENSE', binary.with_name('pzoom.LICENSE'))
    receipt = {'ref': REF, 'source_url': URL, 'experimental': True,
               'build_profile': 'release',
               'rustc': subprocess.check_output(['rustc', '--version'], text=True).strip(),
               'lock_sha256': hashlib.sha256(lock.read_bytes()).hexdigest(),
               'sha256': hashlib.sha256(binary.read_bytes()).hexdigest()}
    binary.with_name('pzoom.provenance.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
