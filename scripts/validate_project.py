#!/usr/bin/env python3
"""Structural evidence-contract validator. Does NOT prove a theorem or verify semantic entailment."""
from __future__ import annotations
import argparse,hashlib,json,re,sys
from pathlib import Path
KINDS={'code','measurement','estimate','proof','literature','hypothesis'}
REQUIRES={
'code_behavior':{'code'},'empirical_quality':{'measurement'},'runtime_speedup':{'measurement'},
'memory_reduction':{'measurement'},'theory_guarantee':{'proof'},'distribution_preservation':{'proof'},
'novelty_first':{'literature'},'estimated_efficiency':{'estimate'},'mechanism_causal':{'measurement','proof'}}

def validate(ledger:dict, repo:Path|None=None, draft:str='', strict:bool=False)->dict:
    errors,warnings=[],[]
    if not isinstance(ledger,dict): return {'ok':False,'errors':['ledger-not-object'],'warnings':[]}
    evs,claims=ledger.get('evidence',[]),ledger.get('claims',[])
    if not isinstance(evs,list) or not isinstance(claims,list):
        return {'ok':False,'errors':['records-must-be-lists'],'warnings':[]}
    lookup={}
    for e in evs:
        if not isinstance(e,dict):errors.append('malformed-evidence');continue
        eid=e.get('id')
        if not isinstance(eid,str) or not eid:errors.append('missing-evidence-id');continue
        if eid in lookup:errors.append(f'duplicate-evidence:{eid}')
        lookup[eid]=e
        if e.get('kind') not in KINDS:errors.append(f'bad-evidence-kind:{eid}')
        loc=e.get('locator',{})
        if not isinstance(loc,dict) or not any(loc.get(k) for k in ('path','url','description')):
            errors.append(f'missing-locator:{eid}');continue
        if repo is not None and loc.get('path'):
            try:
                file=(repo/loc['path']).resolve();file.relative_to(repo.resolve())
                if not file.is_file():errors.append(f'missing-file:{eid}');continue
                if 'lines' in loc:
                    lines=loc['lines']
                    if (not isinstance(lines,list) or len(lines)!=2 or not all(isinstance(v,int) for v in lines)
                        or lines[0]<1 or lines[1]<lines[0]):errors.append(f'invalid-lines:{eid}')
                    else:
                        count=len(file.read_text(encoding='utf-8').splitlines())
                        if lines[1]>count:errors.append(f'lines-out-of-range:{eid}')
                if e.get('sha256'):
                    h=hashlib.sha256()
                    with file.open('rb') as handle:
                        for block in iter(lambda:handle.read(1024*1024),b''):h.update(block)
                    if h.hexdigest()!=e['sha256']:errors.append(f'hash-mismatch:{eid}')
            except (ValueError,TypeError):errors.append(f'path-outside-repo:{eid}')
            except (OSError,UnicodeError):errors.append(f'unreadable-file:{eid}')
    claim_ids=set()
    for c in claims:
        if not isinstance(c,dict):errors.append('malformed-claim');continue
        cid=c.get('id')
        if not isinstance(cid,str) or not cid:errors.append('missing-claim-id');continue
        if cid in claim_ids:errors.append(f'duplicate-claim:{cid}')
        claim_ids.add(cid)
        ids=c.get('evidence_ids',[])
        if not isinstance(ids,list) or not all(isinstance(v,str) for v in ids):errors.append(f'bad-evidence-ids:{cid}');continue
        for eid in ids:
            if eid not in lookup:errors.append(f'unknown-evidence:{cid}:{eid}')
        if c.get('status')!='verified':
            (errors if strict else warnings).append(f'unverified-claim:{cid}');continue
        if not c.get('scope'):errors.append(f'missing-scope:{cid}')
        kinds={lookup[i].get('kind') for i in ids if i in lookup}
        kind=c.get('kind')
        if kind not in REQUIRES:errors.append(f'unknown-claim-kind:{cid}');continue
        if not kinds.intersection(REQUIRES[kind]):errors.append(f'wrong-evidence-type:{cid}')
        if kind=='runtime_speedup' and c.get('protocol',{}).get('matched_baseline') is not True:
            errors.append(f'no-matched-runtime-baseline:{cid}')
        if kind in {'theory_guarantee','distribution_preservation'}:
            if not c.get('assumptions') or c.get('proof_review_status')!='reviewed':
                errors.append(f'unreviewed-or-unscoped-proof:{cid}')
        if kind=='novelty_first' and not c.get('search_record'):
            errors.append(f'first-claim-without-search:{cid}')
        if kind=='mechanism_causal' and not c.get('intervention_or_identification'):
            errors.append(f'causal-claim-without-identification:{cid}')
    for namespace,ref in re.findall(r'\[(E|C):([^\]]+)\]',draft):
        if ref not in (lookup if namespace=='E' else claim_ids):errors.append(f'unknown-draft-reference:{namespace}:{ref}')
    if re.search(r'\[待(?:实验|证明|核验|补充)[^\]]*\]',draft):
        (errors if strict else warnings).append('unresolved-draft-placeholders')
    return {'ok':not errors,'errors':errors,'warnings':warnings,
            'scope':'Structural/type/path checks only. A pass is NOT scientific validation or full-language fact checking.'}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,required=True)
    p.add_argument('--repo',type=Path);p.add_argument('--strict',action='store_true');a=p.parse_args()
    try:
        ledger=json.loads((a.project/'evidence.json').read_text(encoding='utf-8'))
        d=a.project/'draft_annotated.md';draft=d.read_text(encoding='utf-8') if d.exists() else ''
        result=validate(ledger,a.repo,draft,a.strict);print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result['ok'] else 1
    except (OSError,ValueError) as exc: print(f'ERROR: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
