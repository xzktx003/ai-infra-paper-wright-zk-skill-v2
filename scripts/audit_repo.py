#!/usr/bin/env python3
"""Read-only repository inventory. Does NOT execute/import project code or infer novelty."""
from __future__ import annotations
import argparse, ast, hashlib, json, os, sys
from pathlib import Path

EXCLUDE = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.agents', '.claude',
           'checkpoints', 'weights', 'wandb', '.ssh'}
SUFFIXES = {'.py', '.md', '.txt', '.json', '.jsonl', '.yaml', '.yml', '.toml', '.csv', '.log', '.sh', '.cu', '.cpp', '.h'}
SECRET = {'.env', 'credentials.json', 'id_rsa', 'id_ed25519', 'secrets.json'}

def audit(repo: Path, max_files: int = 1000, max_bytes: int = 256_000) -> dict:
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError(f'Repository is not a directory: {repo}')
    records, warnings = [], []
    stop = False
    for base, dirs, names in os.walk(repo, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE and not d.startswith('.') and not (Path(base)/d).is_symlink())
        for name in sorted(names):
            p = Path(base)/name
            if name in SECRET or name.startswith('.env') or p.is_symlink() or p.suffix.lower() not in SUFFIXES:
                continue
            if len(records) >= max_files:
                warnings.append(f'File limit {max_files} reached; inventory is PARTIAL.')
                stop = True
                break
            rec = {'path': str(p.relative_to(repo)), 'bytes': p.stat().st_size,
                   'content_inspected': False, 'meaning': 'file metadata only'}
            if p.stat().st_size <= max_bytes:
                try:
                    data = p.read_bytes()
                    rec.update(sha256=hashlib.sha256(data).hexdigest())
                    text = data.decode('utf-8')
                    rec['line_count'] = len(text.splitlines())
                    if p.suffix == '.py':
                        tree = ast.parse(text, filename=str(p))
                        rec['symbols'] = [{'name': n.name, 'kind': type(n).__name__,
                                           'start': n.lineno, 'end': getattr(n, 'end_lineno', n.lineno)}
                                          for n in ast.walk(tree)
                                          if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                        rec['meaning'] = 'AST symbol inventory only; algorithm semantics NOT verified'
                        rec['content_inspected'] = True
                except (OSError, UnicodeDecodeError, SyntaxError) as exc:
                    rec['note'] = f'Not parsed: {type(exc).__name__}'
            else:
                rec['note'] = 'Over byte limit; no content read or hashed'
            records.append(rec)
        if stop:
            break
    return {'repository': str(repo), 'read_only': True, 'project_code_executed': False,
            'partial': bool(warnings), 'warnings': warnings, 'files': records,
            'limits': {'max_files': max_files, 'max_bytes': max_bytes},
            'next': 'Agent must read relevant files and populate evidence; inventory is not scientific analysis.'}

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', required=True, type=Path)
    p.add_argument('--out', type=Path)
    p.add_argument('--max-files', type=int, default=1000)
    p.add_argument('--max-bytes', type=int, default=256_000)
    a=p.parse_args()
    try:
        if min(a.max_files,a.max_bytes) < 1: raise ValueError('Limits must be positive')
        result=json.dumps(audit(a.repo,a.max_files,a.max_bytes), ensure_ascii=False, indent=2)
        if a.out:
            a.out.parent.mkdir(parents=True,exist_ok=True)
            with a.out.open('x',encoding='utf-8') as f: f.write(result+'\n')
        else: print(result)
        return 0
    except (OSError,ValueError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
