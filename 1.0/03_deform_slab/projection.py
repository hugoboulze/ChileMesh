#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: garaud, boulze

From https://stackoverflow.com/a/32529589/7212665

Make a projection of a point on the surface of a triangle

"""

# =============================================================================
import numpy as np
# =============================================================================


def points_to_triangles(points, triangles):
    with np.errstate(all='ignore'):

        # Unpack triangle points
        p0,p1,p2 = np.asarray(triangles).swapaxes(0,1)

        # Calculate triangle edges
        e0 = p1-p0
        e1 = p2-p0
        a = np.einsum('...i,...i', e0, e0)
        b = np.einsum('...i,...i', e0, e1)
        c = np.einsum('...i,...i', e1, e1)

        # Calculate determinant and denominator
        det = a*c - b*b
        invDet = 1. / det
        denom = a-2*b+c

        # Project to the edges
        p  = p0-points[:,np.newaxis]
        d = np.einsum('...i,...i', e0, p)
        e = np.einsum('...i,...i', e1, p)
        u = b*e - c*d
        v = b*d - a*e

        # Calculate numerators
        bd = b+d
        ce = c+e
        numer0 = (ce - bd) / denom
        numer1 = (c+e-b-d) / denom
        da = -d/a
        ec = -e/c


        # Vectorize test conditions
        m0 = u + v < det
        m1 = u < 0
        m2 = v < 0
        m3 = d < 0
        m4 = (a+d > b+e)
        m5 = ce > bd

        t0 =  m0 &  m1 &  m2 &  m3
        t1 =  m0 &  m1 &  m2 & ~m3
        t2 =  m0 &  m1 & ~m2
        t3 =  m0 & ~m1 &  m2
        t4 =  m0 & ~m1 & ~m2
        t5 = ~m0 &  m1 &  m5
        t6 = ~m0 &  m1 & ~m5
        t7 = ~m0 &  m2 &  m4
        t8 = ~m0 &  m2 & ~m4
        t9 = ~m0 & ~m1 & ~m2

        u = np.where(t0, np.clip(da, 0, 1), u)
        v = np.where(t0, 0, v)
        u = np.where(t1, 0, u)
        v = np.where(t1, 0, v)
        u = np.where(t2, 0, u)
        v = np.where(t2, np.clip(ec, 0, 1), v)
        u = np.where(t3, np.clip(da, 0, 1), u)
        v = np.where(t3, 0, v)
        u *= np.where(t4, invDet, 1)
        v *= np.where(t4, invDet, 1)
        u = np.where(t5, np.clip(numer0, 0, 1), u)
        v = np.where(t5, 1 - u, v)
        u = np.where(t6, 0, u)
        v = np.where(t6, 1, v)
        u = np.where(t7, np.clip(numer1, 0, 1), u)
        v = np.where(t7, 1-u, v)
        u = np.where(t8, 1, u)
        v = np.where(t8, 0, v)
        u = np.where(t9, np.clip(numer1, 0, 1), u)
        v = np.where(t9, 1-u, v)


        # Return closest points
        return (p0.T +  u[:, np.newaxis] * e0.T + v[:, np.newaxis] * e1.T).swapaxes(2,1)

def point_to_triangle(point, triangle):
    points = point.reshape(1,-1)
    triangles = triangle.reshape(1,3,3)
    return points_to_triangles(points, triangles).flatten()


if __name__ == "__main__":

    ### TEST

    triangle = np.array([[0, 0, 0],
                         [1, 0, 0],
                         [0, 1, 0]], dtype=np.float64)

    triangles = triangle.reshape(1,3,3)

    def test_it(lpt):
        pt = np.array(lpt, dtype=np.float64)
        pts = pt.reshape(1,-1)
        proj = points_to_triangles(pts, triangles)
        print(pt, "->", proj)
        return proj


    test_it([1,0,0])
    test_it([0,1,0])
    test_it([0.5,0.5,0])
    test_it([1,1,0])
    test_it([1,1,10])
    test_it([1/3,1/3,100])

    def test_it2(lpt):
        pt = np.array(lpt, dtype=np.float64)
        proj = point_to_triangle(pt, triangle)
        print(pt, "->", proj)
        return proj

    test_it2([1,0,0])
    test_it2([0,1,0])
    test_it2([0.5,0.5,0])
    test_it2([1,1,0])
    test_it2([1,1,10])
    test_it2([1/3,1/3,100])
