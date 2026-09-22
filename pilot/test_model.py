"""Meaningful geometry and probability checks; no environment mutation."""
import math
import unittest

import numpy as np

from model import (D, G, S, chi_square_quantile, confidence_interval,
                   contains, fit, linear_extrema)


class GeometryTests(unittest.TestCase):
    def test_unconstrained_ellipse_matches_support_function(self):
        a = np.array([[40., 7.], [7., 20.]])
        center = np.array([.5, .5])
        result = linear_extrema(a, center, .08)
        half = math.sqrt(.08 * G@np.linalg.solve(a,G))
        self.assertAlmostEqual(result[0], -half, places=10)
        self.assertAlmostEqual(result[1], half, places=10)

    def test_box_clipped_extrema_enclose_dense_grid_and_attain_bounds(self):
        rng = np.random.default_rng(2371)
        axis = np.linspace(0,1,501)
        xx, yy = np.meshgrid(axis,axis)
        grid = np.column_stack([xx.ravel(),yy.ravel()])
        for _ in range(12):
            b = rng.normal(size=(2,2))
            a = b.T@b + .03*np.eye(2)
            center = rng.uniform(-.25,1.25,size=2)
            radius2 = rng.uniform(.01,.3)
            result = linear_extrema(a,center,radius2)
            offsets = grid-center
            mask = np.einsum('ni,ij,nj->n',offsets,a,offsets) <= radius2
            if np.any(mask):
                self.assertIsNotNone(result)
                brute = grid[mask]@G
                self.assertLessEqual(result[0], brute.min()+1e-8)
                self.assertGreaterEqual(result[1], brute.max()-1e-8)
                self.assertLess(brute.min()-result[0], .008)
                self.assertLess(result[1]-brute.max(), .008)
                for endpoint in result[2:]:
                    self.assertTrue(contains(a,center,radius2,endpoint))

    def test_null_direction_does_not_shrink(self):
        widths=[]
        aligned=[]
        for n in (8,8192):
            x=np.tile(S,(n,1))
            a,center,rank=fit(x,x@np.array([.6,.4]))
            radius2,result=confidence_interval(a,center,rank,.15,.05)
            widths.append(result[1]-result[0])
            projected=linear_extrema(a,center,radius2,S)
            aligned.append(projected[1]-projected[0])
        self.assertAlmostEqual(widths[0],2.)
        self.assertAlmostEqual(widths[1],2.)
        self.assertLess(aligned[1],aligned[0]/20)

    def test_full_rank_shrinks_as_sqrt_n(self):
        widths=[]
        for n in (20,80):
            x=np.tile(np.stack([S,D]),(n//2,1))
            a,center,rank=fit(x,x@np.array([.6,.4]))
            _,result=confidence_interval(a,center,rank,.15,.05)
            widths.append(result[1]-result[0])
        self.assertAlmostEqual(widths[0]/widths[1],2.,places=8)

    def test_empty_set(self):
        self.assertIsNone(linear_extrema(np.eye(2),np.array([3.,3.]),.01))

    def test_rank_zero_is_entire_box(self):
        result=linear_extrema(np.zeros((2,2)),np.zeros(2),0.)
        self.assertEqual(result[:2],(-1.,1.))

    def test_exact_ambiguity_witness(self):
        a=np.array([.25,.65]); b=np.array([.65,.25])
        self.assertAlmostEqual(S@a,S@b)
        self.assertLess(G@a,0.)
        self.assertGreater(G@b,0.)

    def test_known_noise_pivot_monte_carlo(self):
        rng=np.random.default_rng(8421)
        for rank in (1,2):
            values=np.sum(rng.normal(size=(20000,rank))**2,axis=1)
            coverage=np.mean(values<=chi_square_quantile(rank,.05))
            self.assertLess(abs(coverage-.95),.008)


if __name__ == '__main__':
    unittest.main(verbosity=2)
