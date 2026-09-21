#!/usr/bin/env python3
"""Rule-based candidate routing from EXPLICIT declared features, not automatic research understanding."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
RULES={
'O1':{'controlled_observation':3,'minimal_intervention':2},
'O2':{'proxy_mismatch':4,'intervention_validated_signal':2},
'O3':{'prior_scaling_ceiling':4,'new_failure_after_relaxation':3},
'M1':{'function_invariance':4,'transformation_design':2},
'M2':{'combinatorial_structure':4,'structure_enables_solver':3},
'M3':{'objective_reformulation':3,'information_reformulation':4},
'M4':{'noncommutativity':4,'joint_compression':3},
'C1':{'distinct_failure_modes':3,'independent_components':2},
'C2':{'coarse_to_fine':4,'preserve_then_restore':4},
'C3':{'two_sided_dilemma':4,'unified_bridge':3},
'S1':{'bottleneck_shift':4,'workload_profiling':3},
'S2':{'hardware_constrains_algorithm':4,'format_kernel_codesign':3},
'S3':{'serial_dependency':3,'asynchronous_execution':4,'fallback_design':2},
'U1':{'understanding_primary':3,'alternative_mechanisms':3},
'U2':{'scaling_law':4,'heldout_prediction':3},
'U3':{'assumption_counterexample':4,'negative_result':3},
'T1':{'theory_primary':4,'upper_lower_bounds':3},
'T2':{'theory_primary':2,'canonical_decomposition':5},
'P1':{'new_setting':3,'problem_contract':3},
'P2':{'benchmark_primary':4,'evaluation_gap':3}}

def route(profile:dict)->dict:
    if not isinstance(profile,dict):raise ValueError('Profile must be a JSON object')
    f=profile.get('features',{})
    if not isinstance(f,dict):raise ValueError('features must be an object of true/false values')
    bad=[k for k,v in f.items() if not isinstance(v,bool)]
    if bad:raise ValueError('Feature values must be booleans: '+', '.join(bad))
    known=set().union(*(x.keys() for x in RULES.values()))
    unknown=sorted(set(f)-known)
    candidates=[]
    for tid,weights in RULES.items():
        reasons=[k for k in weights if f.get(k) is True]
        score=sum(weights[k] for k in reasons)
        if score: candidates.append({'template':tid,'rule_score':score,'declared_features':reasons})
    goal=profile.get('paper_goal','unknown')
    preferred={'theory':{'T1','T2'},'understanding':{'U1','U2','U3'},'benchmark':{'P2'}}.get(goal,set())
    for c in candidates:
        if c['template'] in preferred:c['rule_score']+=3;c['goal_adjustment']=goal
    candidates.sort(key=lambda c:(-c['rule_score'],c['template']))
    edges=profile.get('edges',[])
    kinds={e.get('kind') for e in edges if isinstance(e,dict)}
    relations=[]
    if 'definition_dependency' in kinds:relations.append('R2:strict-definition-dependency')
    if 'initialization_dependency' in kinds:relations.append('R2:alternative-start-ablation-needed')
    if 'theorem_enables' in kinds:relations.append('R4')
    if 'auxiliary' in kinds:relations.append('R5')
    if 'iterative' in kinds:relations.append('R7')
    if f.get('independent_components'):relations.append('R1:independent-definition')
    if f.get('format_kernel_codesign') or f.get('asynchronous_execution'):relations.append('R6')
    if 'execution' in kinds and len(kinds)==1:relations.append('execution-order-only:scientific-dependency-undetermined')
    return {'status':'provisional' if candidates else 'needs_diagnosis',
            'candidates':candidates[:3], 'relations':relations,
            'unknown_features':unknown,
            'warning':'Scores express explicit-rule matches, not truth, novelty, writing quality, or acceptance probability. Read source evidence before selection.'}

def main()->int:
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('profile',type=Path);a.add_argument('--out',type=Path);x=a.parse_args()
    try:
        data=json.dumps(route(json.loads(x.profile.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2)
        if x.out:
            with x.out.open('x',encoding='utf-8') as f:f.write(data+'\n')
        else:print(data)
        return 0
    except (OSError,ValueError) as exc:print(f'ERROR: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
