#!/usr/bin/env python3
"""Create a NEW papers/vN folder. Never overwrites previous drafts or runs experiments."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

PROFILE={
  'schema_version':'1.0','status':'needs_repository_diagnosis',
  'project_name':'','repository':'','language':'zh-CN',
  'paper_goal':'unknown','problem':'','main_claim':'','resource_wall':[],
  'features':{}, 'components':[], 'edges':[], 'constraints':{
    'default_read_only':True,'run_experiments':False,'max_gpus_if_authorized':1},
  'venue_profile':{'venue':'','year':None,'track':'','official_rules_url':'','checked_on':None},
  'routing_justification':'','selected_template':None,'secondary_template':None,
  'source_papers':[], 'unknowns':[]}
HEADERS={
'narrative_diagnosis.md':'研究诊断\n\n待分析仓库与证据；不是依据代码名称编造动机。',
'paragraph_plan.md':'段落计划\n\n每段填写功能、证据ID、读者问题、过渡、禁写主张与篇幅。',
'experiment_gaps.md':'待验证问题\n\n按被威胁主张、替代解释、最低成本实验及预算填写；不自动执行。',
'draft_annotated.md':'中文标注初稿\n\n尚未起草。保留 [E:E01] 与 [待实验:E02] 等证据状态。',
'review_report.md':'逆向审查\n\n检查主张、证据、比较公平性与边界；不预测录用概率。',
'CHANGELOG.md':'版本记录\n\n本版本新建；不得覆盖既有实验结果或改代码迎合故事。'}

def scaffold(repo: Path) -> Path:
    repo=repo.resolve()
    if not repo.is_dir(): raise ValueError('Repository directory does not exist')
    base=repo/'papers'; base.mkdir(exist_ok=True)
    versions=[int(m.group(1)) for p in base.iterdir() if (m:=re.fullmatch(r'v(\d+)',p.name))]
    n=max(versions,default=0)+1
    while True:
        out=base/f'v{n}'
        try: out.mkdir(); break
        except FileExistsError: n+=1
    profile=json.loads(json.dumps(PROFILE)); profile['repository']=str(repo)
    (out/'paper_profile.json').write_text(json.dumps(profile,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'evidence.json').write_text(json.dumps({'schema_version':'1.0','evidence':[],'claims':[]},indent=2)+'\n',encoding='utf-8')
    for name,txt in HEADERS.items(): (out/name).write_text('# '+txt+'\n',encoding='utf-8')
    (out/'references.bib').write_text('% Add only verified bibliographic records. No invented references.\n',encoding='utf-8')
    return out

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);a=p.parse_args()
    try: print(scaffold(a.repo));return 0
    except (OSError,ValueError) as exc: print(f'ERROR: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
