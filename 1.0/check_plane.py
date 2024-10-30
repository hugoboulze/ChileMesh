#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Oct  4 10:13:28 2021

@author: boulze, garaud

Check that face.1 and face.2 (north and south extremities of the subduction interface) are planes

"""


# =============================================================================
import numpy as np
import zset
# =============================================================================

p = zset.Problem(mesh_file='tmp3.geof')
m = p.mesh


for bset in 'face.1', 'face.2':
    f1 = m.bsets[bset]
    n = f1.normals()
    nn= n-n[0]
    print(bset, np.min(nn), np.max(nn), n[0])


