from pathlib import Path
import hashlib, json

root = Path(__file__).resolve().parent.parent / 'sessions/05'
manifest = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and p.name != 'manifest.json'}
(root / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print('Updated manifest:', len(manifest), 'files')
