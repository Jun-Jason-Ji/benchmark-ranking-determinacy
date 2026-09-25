import math
import unittest
import analyze_torque as a

class SecondaryChecks(unittest.TestCase):
    def test_direction_selected_is_two_sided(self):
        for sign in [-1,1]:
            r=a.sign_inference([sign]*8)
            self.assertAlmostEqual(r['two_sided_p'],2/256)
            self.assertTrue(r['reject_at_005'])
    def test_seven_not_significant(self):
        self.assertAlmostEqual(a.sign_inference([-1]*7+[1])['two_sided_p'],18/256)
        self.assertFalse(a.sign_inference([-1]*7+[1])['reject_at_005'])
    def test_ties_retained(self):
        r=a.sign_inference([1]*7+[0]);self.assertEqual(r['zero_blocks'],1)
        self.assertAlmostEqual(r['two_sided_p'],18/256)
    def test_all_zero_not_equivalence(self):
        r=a.sign_inference([0]*8);self.assertEqual(r['two_sided_p'],1)
        self.assertFalse(a.mean_inference([0]*8)['t_working_model']['interval_available'])
    def test_incomplete_rejected(self):
        with self.assertRaises(ValueError):a.sign_inference([-1]*7)
        with self.assertRaises(ValueError):a.mean_inference([-1]*7)
    def test_exact_range(self):
        with self.assertRaises(ValueError):a.sign_inference([49]*8)
        self.assertAlmostEqual(a.mean_inference([-48]*8)['bounded_mean']['radius'],math.sqrt(math.log(40)))
    def test_holm_handles_shared_baseline_without_independence(self):
        self.assertEqual(a.holm_two([1/256,2/256]),[2/256,2/256])
        self.assertEqual(a.holm_two([9/256,2/256]),[9/256,4/256])
        self.assertEqual(a.holm_two([.04,.04]),[.08,.08])
    def test_direction_not_mean(self):
        r=a.sign_inference([-1]*7+[48]);self.assertEqual(r['negative_blocks'],7)
        self.assertGreater(a.mean_inference([-1]*7+[48])['t_working_model']['mean'],0)

if __name__=='__main__':unittest.main(verbosity=2)
