#!/usr/bin/env python3
"""Prepare exact Mago releases and an immutable source commit, without moving pins."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'harness'))
from compare import profiles_from


def prepare(profile: dict, source_tree: Path | None, jobs: int) -> dict:
    binary = ROOT / profile['binary']
    receipt = binary.with_name(binary.name + '.provenance.json')
    if binary.is_file() and receipt.is_file():
        previous = json.loads(receipt.read_text())
        if (previous.get('ref') == profile['ref']
                and previous.get('build_profile') == profile.get('build_profile')
                and previous.get('sha256') == hashlib.sha256(binary.read_bytes()).hexdigest()):
            print(f"Already prepared: {profile['label']}", flush=True)
            return previous
    binary.parent.mkdir(parents=True, exist_ok=True)
    if profile['kind'] == 'release':
        if platform.system() != 'Linux' or platform.machine() != 'x86_64':
            raise RuntimeError('this release matrix uses Linux x86_64 binaries')
        version = profile['ref']
        url = (f'https://github.com/carthage-software/mago/releases/download/{version}/'
               f'mago-{version}-x86_64-unknown-linux-gnu.tar.gz')
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / 'mago.tar.gz'
            subprocess.run(['curl', '--fail', '--location', '--retry', '3', '--silent',
                            '--show-error', '--output', str(archive), url], check=True)
            with tarfile.open(archive) as packed:
                members = [member for member in packed.getmembers()
                           if member.isfile() and Path(member.name).name == 'mago']
                if len(members) != 1:
                    raise RuntimeError('expected exactly one Mago executable in the release archive')
                with packed.extractfile(members[0]) as source, binary.open('wb') as destination:
                    shutil.copyfileobj(source, destination)
        source_url = f'https://github.com/carthage-software/mago/releases/tag/{version}'
    else:
        source = source_tree or ROOT / '.tools-alt' / 'mago-source' / profile['ref']
        if not source.exists():
            source.mkdir(parents=True)
            subprocess.run(['git', 'init', str(source)], check=True)
            subprocess.run(['git', '-C', str(source), 'fetch', '--depth', '1',
                            'https://github.com/carthage-software/mago.git', profile['ref']], check=True)
            subprocess.run(['git', '-C', str(source), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
        actual = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
        dirty = subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip()
        if actual != profile['ref'] or dirty:
            raise RuntimeError('source checkout must be clean and match the configured full commit')
        command = ['cargo', 'build', '--locked', '--bin', 'mago', '-j', str(jobs)]
        build_profile = profile.get('build_profile', 'dev')
        if build_profile == 'release':
            command.append('--release')
        elif build_profile != 'dev':
            raise ValueError('build_profile must be dev or release')
        subprocess.run(command, cwd=source, check=True)
        target = Path(os.environ.get('CARGO_TARGET_DIR', str(source / 'target')))
        shutil.copy2(target / ('release' if build_profile == 'release' else 'debug') / 'mago', binary)
        source_url = f"https://github.com/carthage-software/mago/commit/{profile['ref']}"
    binary.chmod(0o755)
    version = subprocess.check_output([str(binary), '--version'], text=True).strip()
    if profile['kind'] == 'release' and version != f"mago {profile['ref']}":
        raise RuntimeError(f"release version mismatch: {version}")
    proof = {'kind': profile['kind'], 'ref': profile['ref'], 'source_url': source_url,
             'observed_version': version, 'sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
             'build_profile': profile.get('build_profile')}
    receipt.write_text(json.dumps(proof, indent=2) + '\n')
    print(f"Prepared {profile['label']}: {proof['sha256']}", flush=True)
    return proof


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=str(ROOT / 'tools/mago-matrix.json'))
    parser.add_argument('--source-tree', type=Path, help='reuse a clean checkout of the exact configured commit')
    parser.add_argument('--jobs', type=int, default=2)
    args = parser.parse_args()
    for profile in profiles_from(args.config):
        prepare(profile, args.source_tree, args.jobs)


if __name__ == '__main__':
    main()
