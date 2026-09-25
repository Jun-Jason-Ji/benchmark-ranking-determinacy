import math
import unittest
import analyze_confirmation as a

class FrozenAnalysisChecks(unittest.TestCase):
    def test_eight_negative(self):
        r=a.primary_inference([-1]*8)
        self.assertAlmostEqual(r['one_sided_exact_binomial_p'],1/256)
        self.assertTrue(r['reject_at_005'])
        self.assertGreater(r['one_sided_exact_95_lower_bound'],.5)

    def test_seven_negative(self):
        r=a.primary_inference([-1]*7+[1])
        self.assertAlmostEqual(r['one_sided_exact_binomial_p'],9/256)
        self.assertTrue(r['reject_at_005'])

    def test_zeros_are_not_removed(self):
        r=a.primary_inference([-1]*6+[0,0])
        self.assertEqual(r['n_blocks'],8)
        self.assertEqual(r['zero_blocks'],2)
        self.assertFalse(r['reject_at_005'])

    def test_no_partial_pvalue(self):
        with self.assertRaises(ValueError):a.primary_inference([-1]*7)

    def test_direction_is_not_mean(self):
        # Seven negative changes and one large positive change: sign significant, mean positive.
        data=[-1]*7+[48]
        self.assertTrue(a.primary_inference(data)['reject_at_005'])
        self.assertGreater(a.secondary_inference(data)['t_working_model']['mean'],0)

    def test_difference_of_gaps_range(self):
        x=a.secondary_inference([-1,-2,-3,-4,-5,-6,-7,-8])['bounded_mean']
        self.assertEqual(x['block_range'],[-2,2])
        self.assertAlmostEqual(x['radius'],math.sqrt(math.log(40)))

    def test_zero_observed_variance_not_point_ci(self):
        r=a.secondary_inference([-2]*8)
        self.assertFalse(r['t_working_model']['interval_available'])
        self.assertGreater(r['bounded_mean']['upper'],r['bounded_mean']['lower'])

    def test_full_record_gate(self):
        rows=[dict(episode_id=i,success=True,policy='octo-small',env_id=a.ENV,condition='nominal',steps=60,policy_seed=100+i)for i in range(24)]
        self.assertEqual(sum(a.validate_rows(rows,'octo-small','nominal',100).values()),24)
        rows[-1]['episode_id']=0
        with self.assertRaises(ValueError):a.validate_rows(rows,'octo-small','nominal',100)

if __name__=='__main__':unittest.main(verbosity=2)
