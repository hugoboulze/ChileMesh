#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 10:08:31 2022

@author: boulze, garaud

Check that nodes from COMP-X1-X2 are all between X1 and X2 depth

"""

# =============================================================================
import numpy as np
import zset
import sys
import matplotlib.pyplot as plt
from constants import zmax, z4km, z54km, z70km, z200km, z270km, z670km, zmin
# =============================================================================

tolerance = 1e-4
scale = 2.5

depth = {'00': scale*zmax, '04': scale*z4km, '54': scale*z54km, '70': scale*z70km,
         '200': scale*z200km, '270': scale*z270km, '670': scale*z670km, 'BOTTOM': scale*zmin}


mesh_path = sys.argv[1] #check end of Step 5, mesh needs to be flat
mesh = zset.Mesh(mesh_path)

node_coords = mesh.nodes_coordinates()

comp_to_check = ['COMP-670-BOTTOM', 'COMP-270-670', 'COMP-200-270', 'COMP-70-200', 'COMP-54-70','COMP-04-54', 'COMP-00-04']

print('#################')
print('CHECK COMP REPORT')
print('#################\n')
print('Tolerance: ' + str(tolerance) + ' km \n')

for comp in comp_to_check:

    mesh.transform('**nset {} *use_elset {} *function 1.;'.format(comp, comp))
    nset_comp = mesh.nsets[comp]
    node_comp = node_coords[nset_comp.mask()]

    Z_node_comp = node_comp[:, 2]

    Z_comp = comp.split('-')[1:]

    depth1 = depth[Z_comp[0]]
    depth2 = depth[Z_comp[1]]

    print('\n ELSET: ' + comp + '\n')

    if not np.all(Z_node_comp < depth1 + tolerance, axis=0):
        print('[ERROR]: Some Nodes found HIGHER than ' + Z_comp[0] + ' km !!!')
    else:
        print('[OK]: All Nodes found LOWER than ' + Z_comp[0] + ' km')

    if not np.all(Z_node_comp > depth2 - tolerance, axis=0):
        print('[ERROR]: Some Nodes found LOWER than ' + Z_comp[1] + ' km !!! \n')
    else:
        print('[OK]: All Nodes found HIGHER than ' + Z_comp[1] + ' km')

    plt.figure()
    plt.scatter(nset_comp.ids(), Z_node_comp)
    plt.xlabel('Node IDS')
    plt.ylabel('Depth (Z axis)')
    plt.title('Depth of '+comp+' nodes')

plt.show()
