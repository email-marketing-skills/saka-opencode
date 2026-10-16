#!/usr/bin/env python3
"""Install skills and merge absent MCP entries without overwriting user work."""
import json, shutil, sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
def install(target):
    target=target.resolve()
    cfg=target/'opencode.json'
    if (target/'opencode.jsonc').exists():
        raise ValueError('opencode.jsonc exists; merge the supplied MCP entries manually to preserve comments.')
    if cfg.is_symlink():raise ValueError('Refusing symlinked configuration.')
    current=json.loads(cfg.read_text()) if cfg.exists() else {}
    incoming=json.loads((root/'opencode.json').read_text())['mcp']
    old=current.get('mcp',{})
    if not isinstance(old,dict):raise ValueError('Existing mcp must be an object.')
    for key,value in incoming.items():
        if key in old and old[key]!=value:raise ValueError('Existing MCP entry differs: '+key)
    dest=target/'.opencode/skills'
    if any(p.is_symlink() for p in [target/'.opencode',dest]):raise ValueError('Refusing symlinked skill destination.')
    copies=[]
    for src in sorted((root/'skills').iterdir()):
        if not src.is_dir():continue
        out=dest/src.name
        if out.is_symlink():raise ValueError('Refusing symlinked skill: '+src.name)
        if out.exists():
            a={str(p.relative_to(src)):p.read_bytes() for p in src.rglob('*') if p.is_file()}
            b={str(p.relative_to(out)):p.read_bytes() for p in out.rglob('*') if p.is_file()}
            if a!=b:raise ValueError('Existing skill differs: '+src.name)
        else:copies.append((src,out))
    # No mutation before all configuration and skill conflicts have been checked.
    target.mkdir(parents=True,exist_ok=True)
    current['mcp']={**old,**incoming}
    for src,out in copies:shutil.copytree(src,out)
    if not cfg.exists() or json.loads(cfg.read_text())!=current:
        with cfg.open('w') as f:json.dump(current,f,indent=2);f.write('\n')
    print('Installed Saka skills and MCP configuration in',target)

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python3 scripts/install-opencode.py /path/to/project')
    try:install(Path(sys.argv[1]))
    except (ValueError,OSError) as e:raise SystemExit(str(e))
