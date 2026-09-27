from pathlib import Path
import json
import sys
import zlib
import zipfile
import subprocess

root = Path(__file__).resolve().parents[1]
archives = root / 'data/raw/levir_cd_archives'
dataset = root / 'data/raw/levir_cd'
sources = {'train': '18GuoCuBn48oZKAlEo-LrNwABrFhVALU-', 'val': '1BqSt4ueO7XAyQ_84mUjswUSJt13ZBuzG', 'test': '1jj3qJD_grJlgIhUWO09zibRGJe0R4Tn0'}

def fetch(item):
    split, file_id = item
    archive = archives / (split + '.zip')
    archives.mkdir(parents=True, exist_ok=True)
    print(f'Downloading {split}.zip', flush=True)
    if not archive.exists():
        partial = archives / (split + '-curl.zip')
        subprocess.run(['curl.exe', '-L', '--fail', '--connect-timeout', '30', '--max-time', '14400', '--speed-time', '60', '--speed-limit', '1024', '--retry', '3', '--retry-all-errors', '-C', '-', '-o', str(partial), f'https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t'], check=True)
        partial.rename(archive)
    with zipfile.ZipFile(archive) as z:
        bad = z.testzip()
        if bad:
            raise ValueError(f'Corrupt archive member: {bad}')
        members = []
        verified_existing = 0
        for entry in z.infolist():
            if entry.is_dir():
                continue
            parts = Path(entry.filename).parts
            if len(parts) >= 2 and parts[-2] in ('A', 'B', 'label') and parts[-1].lower().endswith('.png'):
                target = dataset / split / parts[-2] / parts[-1]
                if target.exists():
                    if target.stat().st_size != entry.file_size or zlib.crc32(target.read_bytes()) != entry.CRC:
                        raise ValueError(f'Existing file differs from archive: {target}')
                    verified_existing += 1
                    continue
                members.append((entry, target))
        if not members and not verified_existing:
            raise ValueError(f'No dataset PNGs in {split}')
        for entry, target in members:
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(entry) as source, target.open('xb') as dest:
                import shutil
                shutil.copyfileobj(source, dest)
        print(f'{split}: {len(members)} PNGs extracted, {verified_existing} existing PNGs verified; ZIP CRC checks passed', flush=True)
    return split

for split in ('val', 'test', 'train'):
    fetch((split, sources[split]))
(dataset / 'download_source.json').write_text(json.dumps({'source': 'https://justchenhao.github.io/LEVIR/', 'google_drive_file_ids': sources, 'terms': 'Academic use only; commercial use prohibited', 'splits': 'Preserved from provider archives'}, indent=2))
print('All dataset downloads and extractions complete.', flush=True)
subprocess.run([sys.executable, str(root / 'scripts/validate_dataset.py'), str(dataset)], check=True)
