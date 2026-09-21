#!/usr/bin/env python3
"""Deterministic contract tests. No LLM calls, no model training, no paper-quality claims."""
from __future__ import annotations
import io,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_project import validate
from route_profile import route
from scaffold import scaffold
from audit_repo import audit

def ledger(ekind='measurement',ckind='empirical_quality',**extra):
    c={'id':'C01','kind':ckind,'status':'verified','scope':'synthetic fixed protocol', 'evidence_ids':['E01']}
    c.update(extra)
    return {'evidence':[{'id':'E01','kind':ekind,'locator':{'description':'synthetic fixture, not a real experimental finding'}}],'claims':[c]}

class ContractTests(unittest.TestCase):
    def test_code_cannot_prove_runtime(self):
        r=validate(ledger('code','runtime_speedup',protocol={'matched_baseline':True}))
        self.assertIn('wrong-evidence-type:C01',r['errors'])
    def test_estimate_cannot_prove_runtime(self):
        self.assertFalse(validate(ledger('estimate','runtime_speedup',protocol={'matched_baseline':True}))['ok'])
    def test_runtime_needs_matched_protocol(self):
        self.assertFalse(validate(ledger('measurement','runtime_speedup'))['ok'])
    def test_measured_runtime_contract(self):
        self.assertTrue(validate(ledger('measurement','runtime_speedup',protocol={'matched_baseline':True}))['ok'])
    def test_first_claim_needs_search(self):
        self.assertFalse(validate(ledger('literature','novelty_first'))['ok'])
    def test_unknown_evidence(self):
        d=ledger();d['claims'][0]['evidence_ids']=['E-missing']
        self.assertFalse(validate(d)['ok'])
    def test_proof_needs_assumptions(self):
        self.assertFalse(validate(ledger('proof','theory_guarantee'))['ok'])
    def test_theory_no_gpu_required(self):
        d=ledger('proof','theory_guarantee',assumptions=['finite setting'],proof_review_status='reviewed')
        self.assertTrue(validate(d)['ok'])
    def test_distribution_cannot_use_samples_only(self):
        d=ledger('measurement','distribution_preservation',assumptions=['sampling protocol'],proof_review_status='reviewed')
        self.assertFalse(validate(d)['ok'])
    def test_correlation_is_not_causal_identification(self):
        self.assertFalse(validate(ledger('measurement','mechanism_causal'))['ok'])
    def test_draft_allows_proposed_claim(self):
        d=ledger();d['claims'][0]['status']='proposed'
        r=validate(d,draft='结果[待实验:E02]');self.assertTrue(r['ok']);self.assertTrue(r['warnings'])
    def test_strict_rejects_proposed_claim(self):
        d=ledger();d['claims'][0]['status']='proposed'
        self.assertFalse(validate(d,strict=True)['ok'])
    def test_missing_markdown_reference(self):
        self.assertFalse(validate(ledger(),draft='正文[E:E99]')['ok'])
    def test_duplicate_ids(self):
        d=ledger();d['evidence'].append(d['evidence'][0].copy())
        self.assertFalse(validate(d)['ok'])
    def test_empty_profile_abstains(self):
        self.assertEqual(route({})['status'],'needs_diagnosis')
    def test_router_theory_not_forced_phenomenon(self):
        r=route({'paper_goal':'theory','features':{'theory_primary':True,'upper_lower_bounds':True}})
        self.assertEqual(r['candidates'][0]['template'],'T1')
    def test_execution_not_scientific_dependency(self):
        r=route({'edges':[{'kind':'execution'}]})
        self.assertIn('execution-order-only:scientific-dependency-undetermined',r['relations'])
    def test_independence_does_not_imply_stages(self):
        r=route({'features':{'independent_components':True,'distinct_failure_modes':True}})
        self.assertEqual(r['candidates'][0]['template'],'C1')
        self.assertNotIn('R2:strict-definition-dependency',r['relations'])
    def test_router_scaling_law(self):
        r=route({'paper_goal':'understanding','features':{'scaling_law':True,'heldout_prediction':True}})
        self.assertEqual(r['candidates'][0]['template'],'U2')
    def test_invalid_feature_type_rejected(self):
        with self.assertRaises(ValueError):route({'features':{'theory_primary':'yes'}})
    def test_scaffold_never_overwrites(self):
        with tempfile.TemporaryDirectory() as x:
            p=Path(x);a=scaffold(p);(a/'draft_annotated.md').write_text('keep')
            b=scaffold(p);self.assertNotEqual(a,b);self.assertEqual((a/'draft_annotated.md').read_text(),'keep')
    def test_audit_does_not_execute(self):
        with tempfile.TemporaryDirectory() as x:
            p=Path(x);(p/'method.py').write_text("raise RuntimeError('MUST NOT EXECUTE')\ndef f(x):\n    return x\n")
            r=audit(p);self.assertFalse(r['project_code_executed']);self.assertEqual(r['files'][0]['symbols'][0]['name'],'f')
    def test_audit_reports_partial(self):
        with tempfile.TemporaryDirectory() as x:
            p=Path(x);(p/'a.py').write_text('x=1');(p/'b.py').write_text('x=2')
            self.assertTrue(audit(p,max_files=1)['partial'])
    def test_evidence_path_escape(self):
        with tempfile.TemporaryDirectory() as x:
            d=ledger('code','code_behavior');d['evidence'][0]['locator']={'path':'../escape.txt'}
            self.assertFalse(validate(d,Path(x))['ok'])
    def test_invalid_line_range(self):
        with tempfile.TemporaryDirectory() as x:
            p=Path(x);(p/'a.py').write_text('x=1\n')
            d=ledger('code','code_behavior');d['evidence'][0]['locator']={'path':'a.py','lines':[1,20]}
            self.assertFalse(validate(d,p)['ok'])
    def test_semantic_truth_is_out_of_scope(self):
        # A deliberately silly claim demonstrates a real limitation: metadata != truth.
        d=ledger();d['claims'][0]['text']='This fixture asserts a conclusion not semantically checked by this validator.'
        self.assertTrue(validate(d)['ok'])

if __name__=='__main__':
    stream=io.StringIO()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    output={'executed':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
            'passed':result.testsRun-len(result.failures)-len(result.errors),
            'llm_evaluations_run':0,'model_experiments_run':0,
            'scope':'Deterministic schema, routing, path, and read-only behavior checks; NOT research or writing-quality validation.',
            'log':stream.getvalue()}
    (ROOT/'evals/test-results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(stream.getvalue());print(json.dumps({k:v for k,v in output.items() if k!='log'},ensure_ascii=False,indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
