#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: hugob

Create the .geof of the Chilean subduction trench from the trench_chile_34pts

"""

# =============================================================================
import sys
import numpy as np
import zset
# =============================================================================

DIR='./'

infile = sys.argv[1]
coordinates = np.loadtxt(infile)
print("Adding", len(coordinates), "points")

m = zset.Mesh()
m.add_nodes(coordinates)
m.nsets['ALL'].name = 'ChileanFault'
m.save(DIR+'trench_chile.geof')
