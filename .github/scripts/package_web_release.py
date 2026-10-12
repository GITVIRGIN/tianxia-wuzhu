"""Verify the exported runtime and assemble public Web release assets."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest().upper()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', required=True)
    args = parser.parse_args()
    web = json.loads((ROOT / 'web-build-manifest.json').read_text(encoding='utf-8-sig'))
    version = web['build_version']
    if args.tag != f'v{version}-web':
        raise SystemExit('Release tag must match the exported Web version')
    for entry in web['files']:
        path = ROOT / entry['name']
        if path.parent != ROOT or not path.is_file():
            raise SystemExit(f'Invalid runtime file: {entry["name"]}')
        if digest(path) != entry['sha256'].upper() or path.stat().st_size != entry['bytes']:
            raise SystemExit(f'Runtime checksum mismatch: {entry["name"]}')
    notes = ROOT / 'release-assets' / f'v{version}'
    output = ROOT / '.release-output'
    output.mkdir(exist_ok=True)
    payload = [(p, f'dist/browser/{p.name}') for p in sorted(ROOT.glob('index.*'))
               if p.is_file() and not p.name.endswith('.import')]
    payload += [(ROOT / name, f'dist/browser/{name}') for name in ('.nojekyll', 'web-build-manifest.json')]
    payload += [(ROOT / name, name) for name in ('PLAY_BROWSER.cmd', 'PLAY-LOCAL.md')]
    payload += [(ROOT / 'scripts' / name, f'scripts/{name}')
                for name in ('start-browser.ps1', 'serve-web.mjs')]
    payload += [(notes / name, name) for name in ('RELEASE-NOTES.md', 'ACCEPTANCE.md')]
    archive = output / f'TianxiaWuzhu-Web-v{version}.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for path, name in payload:
            info = zipfile.ZipInfo(name, (2026, 10, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            package.writestr(info, path.read_bytes(), compresslevel=9)
    with zipfile.ZipFile(archive) as package:
        if package.testzip() is not None:
            raise SystemExit('ZIP integrity check failed')
        for path, name in payload:
            if hashlib.sha256(package.read(name)).hexdigest().upper() != digest(path):
                raise SystemExit(f'ZIP content mismatch: {name}')
    for name in ('RELEASE-NOTES.md', 'ACCEPTANCE.md'):
        shutil.copyfile(notes / name, output / name)
    shutil.copyfile(ROOT / 'web-build-manifest.json', output / 'web-build-manifest.json')
    manifest = {
        'build_version': version, 'tag': args.tag, 'platform': 'Web',
        'pages_url': 'https://gitvirgin.github.io/tianxia-wuzhu/',
        'source_fingerprint': web['source_fingerprint'],
        'schema_version': web['schema_version'],
        'validation': {'focused_regression': 89, 'full_game_regression': 295,
                       'normal_play_routes': 2, 'grain_procurements_audited': 520,
                       'scope': 'See ACCEPTANCE.md for tested builds and limits'},
        'runtime_files': web['files'],
        'archive': {'name': archive.name, 'bytes': archive.stat().st_size, 'sha256': digest(archive)},
        'native_release_unchanged': 'v0.26.0-r26',
    }
    (output / 'release-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    names = [archive.name, 'RELEASE-NOTES.md', 'ACCEPTANCE.md', 'web-build-manifest.json', 'release-manifest.json']
    (output / 'CHECKSUMS.sha256').write_text(''.join(f'{digest(output / name)}  {name}\n' for name in names), encoding='utf-8')
    print(json.dumps({'version': version, 'zip_bytes': archive.stat().st_size,
                      'runtime_files': len(web['files']), 'zip_entries': len(payload),
                      'source_fingerprint': web['source_fingerprint']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
