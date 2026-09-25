import hashlib
import json
import math
from pathlib import Path
import unittest
import numpy as np
import reanalyze_statistics as a

class StatisticalChecks(unittest.TestCase):
    def test_direction_must_precede_iut(self):
        self.assertEqual(a.iut([[.001,.999],[.999,.001]]),1.)
        self.assertAlmostEqual(a.iut([[.001,.999],[.002,.998]]),.004)

    def test_hoeffding_inverse_interval(self):
        R2=.02; radius=math.sqrt(.5*R2*math.log(2/.05))
        self.assertAlmostEqual(a.iut([a.h_tails(radius,R2)]),.05)
        self.assertGreater(a.iut([a.h_tails(radius-.001,R2)]),.05)

    def test_missing_configuration_is_failure(self):
        with self.assertRaises(ValueError):a.group_config([{'config':0}],2)

    def test_zero_empirical_variance_is_not_exactness(self):
        self.assertFalse(a.block_t([.5,.5,.5])['supported'])
        self.assertFalse(a.block_t([.5])['supported'])

    def test_seed_dependence_increases_range(self):
        ra=[dict(config=c,success=1,seed=c,block='A')for c in range(3)]
        rb=[dict(config=c,success=0,seed=c,block='A')for c in range(3)]
        ep=a.bounded_result(ra,rb,3,'episode',True)
        sd=a.bounded_result(ra,rb,3,'seed',True)
        dr=a.bounded_result(ra,rb,3,'directory',True)
        self.assertAlmostEqual(sd['sum_range_sq'],2*ep['sum_range_sq'])
        self.assertAlmostEqual(dr['sum_range_sq'],4.)
        self.assertFalse(a.bounded_result(ra,rb,3,'seed',False)['supported'])

    def test_block_variance_keeps_cross_configuration_covariance(self):
        # Four configurations all share the same run shock.
        run=np.array([[-1.]*4,[0.]*4,[1.]*4])
        block_var=np.var(run.mean(axis=1),ddof=1)/3
        diagonal_var=np.var(run,axis=0,ddof=1).sum()/3/16
        self.assertAlmostEqual(block_var,4*diagonal_var)

    def test_pair_family_and_scope(self):
        d=json.loads((a.HERE/'ANALYSIS.json').read_text())
        self.assertEqual(len(d['pairs']),17)
        self.assertEqual(sum(len(r['conditions'])==2 for r in d['pairs']),2)
        self.assertEqual(sum(len(r['conditions'])==6 for r in d['pairs']),15)
        m={r['method']:r for r in d['method_comparisons']}
        self.assertEqual((m['legacy_normal']['holm_point'],m['legacy_normal']['holm_envelope']),(9,5))
        self.assertEqual((m['raw_legacy_variance_normal']['holm_point'],m['raw_legacy_variance_normal']['holm_envelope']),(9,5))
        self.assertEqual((m['raw_execution_normal']['holm_point'],m['raw_execution_normal']['holm_envelope']),(9,4))

    def test_inputs_match_pins(self):
        d=json.loads((a.HERE/'INPUT_MANIFEST.json').read_text())
        self.assertEqual(hashlib.sha256((a.HERE/'reanalyze_statistics.py').read_bytes()).hexdigest(),d['script_sha256'])
        for path,meta in d['files'].items():
            self.assertEqual(hashlib.sha256((a.ROOT/path).read_bytes()).hexdigest(),meta['sha256'],path)

if __name__=='__main__':unittest.main(verbosity=2)
