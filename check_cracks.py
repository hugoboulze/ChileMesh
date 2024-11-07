#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Oct  4 10:13:28 2021

@author: boulze, garaud

Use to check if a crack/hole is present in the mesh
To do that, the finess of the mesh is reduced at the minimum
Two mesh geometries are taken into account: SPHE (3D spherical) and FLAT (3D flat)

"""

# =============================================================================
import sys
import zset
# =============================================================================

# retrieve arguments from terminal
mesh_path = sys.argv[1]
geom = sys.argv[2]

if geom not in ['SPHE','FLAT']:
    print("Unkwown mesh geometry")
    exit

mesh = zset.mesh.Mesh(mesh_path)

if geom =='SPHE':
    mesh.transform('**XYZ_to_RThetaPhi')

mesh.transform("**mesh_gems *optim_style -2")
mesh.transform("***shell grep -A 1 Vertices _mesh_out_to_ghs3d.mesh")

print('Number of nodes : ', mesh.nb_nodes)

mesh.save('verif.geof')
