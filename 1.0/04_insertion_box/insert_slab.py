#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 12:00:48 2024

@author: garaud, boulze

Triangulate manually the surface of the box.
Can be used when Zcracks in step 5 fails.

We need to manually label the 4 corners (c1 ... c4)
and the 4 sides of the slab's surface (l1 ... l4)
and decide which sees which.
For l4, there is a little subtlety: the side must be cut in half
because a single corner would create upside-down triangles.

"""

# =============================================================================
import sys
import numpy as np
from zset import Mesh
sys.path.append('../')
from constants import xmin, ymin, zmin, xmax, ymax, zmax
# =============================================================================


# make a 5-sided box (without the top part)
box = Mesh()

corners = np.array([
    [0,0,0],
    [1,0,0],
    [1,1,0],
    [0,1,0],
    [0,0,1],
    [1,0,1],
    [1,1,1],
    [0,1,1]
], dtype=np.float64)
corners[:,0] *= (xmax - xmin)
corners[:,0] += xmin
corners[:,1] *= (ymax - ymin)
corners[:,1] += ymin
corners[:,2] *= (zmax - zmin)
corners[:,2] += zmin

corners[:,2] *= 2.5  # scale by 2.5
box.add_nodes(corners)

five_faces = np.array([
    # oriented outwards
    [1,4,3,2],
    [1,2,6,5],
    [2,6,7,3],
    [3,7,8,4],
    [1,5,8,4]
], dtype=np.int32)
five_faces -=1 # because it expects ranks, not ids
box.add_elements("s3d4", five_faces)

box.save("box.geof")


slab = Mesh('../03_deform_slab/out/slab_deformed_arrondi_FLAT.geof')
slab.transform('**scale 1. 1. 2.5')
slab.save('slab.geo')
# slab.add_nodes(corners) # NotImplementedError: Cannot (currently) add nodes to a non empty mesh
slab.transform('**extract_surface')

slab.transform('**union *add box.geof')


# safety-check
c = slab.nodes_coordinates()[-8:,:]
# box.save/reload adds a little rouding error
np.testing.assert_allclose(c, corners)



# get 4 sides of slab:
surf = slab.nsets['surface-ext'].mask()
face1 = slab.nsets['face.1'].mask()
face2 = slab.nsets['face.2'].mask()
left = slab.nsets['left-ext'].mask()
right = slab.nsets['surface_3'].mask()  # may need manual adjusting
ridges = slab.nsets['RIDGES'].mask()

#zipper = slab.nsets.add('zipper', mask=ridges*surf)
l1 = slab.nsets.add('l1', mask=surf*face1)
l2 = slab.nsets.add('l2', mask=surf*face2)
l3 = slab.nsets.add('l3', mask=surf*left)
l4 = slab.nsets.add('l4', mask=surf*right)


for i in range(1,5):
    slab.transform("**bset l%d *use_nset l%d *function 1.; *use_dimension 1"%(i,i))
    slab.transform("**continuous_liset *liset_name l%d"%i)

slab.transform("**join_bsets zipper *bsets l1 l3 l2 l4")
slab.transform("**continuous_liset *liset_name zipper")
#slab.save('slab.geof')

zipper = slab.bsets['zipper']
connec = zipper.connectivity(False)[1]
connec.shape=(-1,2)

# now draw triangles, using the correct corner and all edges of zipper:
c1,c2,c3,c4 = range(slab.nb_nodes-4, slab.nb_nodes)
start_id = 500000
# handle l1 (sees c2)
edges = slab.bsets['l1'].connectivity(False)[1].reshape(-1,2)
triangles = np.zeros((len(edges), 3), dtype=edges.dtype)
triangles[:,:2] = edges
triangles[:,2] = c2
slab.add_elements('s3d3', triangles, start_id=start_id)
start_id += len(edges)

# handle l2 (sees c1)
edges = slab.bsets['l2'].connectivity(False)[1].reshape(-1,2)
triangles = np.zeros((len(edges), 3), dtype=edges.dtype)
triangles[:,:2] = edges
triangles[:,2] = c1
slab.add_elements('s3d3', triangles, start_id=start_id)
start_id += len(edges)

# handle l3 (sees c1)
edges = slab.bsets['l3'].connectivity(False)[1].reshape(-1,2)
triangles = np.zeros((len(edges), 3), dtype=edges.dtype)
triangles[:,:2] = edges
triangles[:,2] = c1
slab.add_elements('s3d3', triangles, start_id=start_id)
start_id += len(edges)

slab.transform("**inverse_bset *names l4")
# handle l4[:100] (sees c3)
edges = slab.bsets['l4'].connectivity(False)[1].reshape(-1,2)[:100]
triangles = np.zeros((len(edges), 3), dtype=edges.dtype)
triangles[:,:2] = edges
triangles[:,2] = c3
slab.add_elements('s3d3', triangles, start_id=start_id)
start_id += len(edges)

# handle l4[100:] (sees c4)
edges = slab.bsets['l4'].connectivity(False)[1].reshape(-1,2)[100:]
triangles = np.zeros((len(edges), 3), dtype=edges.dtype)
triangles[:,:2] = edges
triangles[:,2] = c4
slab.add_elements('s3d3', triangles, start_id=start_id)
start_id += len(edges)

# # add the 4 missing triangles:
edges = slab.bsets['l1'].connectivity(False)[1].reshape(-1,2)
triangles = np.zeros((4, 3), dtype=edges.dtype)
triangles[0] = [c2, c1, edges[0,0]]
triangles[1] = [c2, c3, edges[-1,-1]]
edges = slab.bsets['l2'].connectivity(False)[1].reshape(-1,2)
triangles[2] = [c4, c1, edges[0,0]]
edges = slab.bsets['l4'].connectivity(False)[1].reshape(-1,2)[100:]
triangles[3] = [c4, c3, edges[0,0]]
slab.add_elements('s3d3', triangles, start_id=start_id)
slab.elsets.add("t1", ids=range(start_id, start_id+1))
slab.elsets.add("t2", ids=range(start_id+1, start_id+2))
slab.elsets.add("t3", ids=range(start_id+2, start_id+3))
slab.elsets.add("t4", ids=range(start_id+3, start_id+4))

slab.save('slab-inserted.geo')
