#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: boulze 
"""

import zset
import numpy as np

m = zset.Mesh('./mesh-before-remeshing.geo')

#m.transform('**extract_surface *elset SLAB')
#m.transform('**bset plan_de_faille_to_keep *use_bset surface_2 *function (z > 0.984303876 -1.e-4)*(z< 1.0+ 1.e-5);')
#m.transform('**remove_set *bsets_start_with surface')   

m.transform('**elset_near_nset *nset fault_plane *radius 5. *distance_file FAULT_PLANE_DST')



db = zset.io.Reader('FAULT_PLANE_DST.ut')
distance = db.get_nodal('dst')
distance = distance[:, np.newaxis] 

size = np.zeros(distance.shape)

for i,d in enumerate(distance):
    
    if d<= 0.04:
        size[i]= 0.005
    if 0.04 < d <= 0.15:
        size[i]= 0.01
    if 0.15 < d:
        size[i]= 0.04

np.savetxt('metric_cvg.dat', np.hstack((m.nodes_coordinates(), size)), comments="", header="%d" %m.nb_nodes)
#m.save('mesh-before-remeshing_cvg.geo')
