#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: boulze, garaud

Main file that manage the iterative deformation of the slab

"""

# =============================================================================
import numpy as np
import zset
import projection
# =============================================================================

DIR = './'

slab_2_Hayes_XYZ = np.genfromtxt('../../01_surface_slab/out/slabSurf_0.1deg_SPHE.csv', delimiter=',')
bad_slab = zset.Mesh('../../02_slab_2D_to_3D/out/slab_refined_FLAT.geof')

# to well capture strong curvatures in the slab geometry, we decompose the
# slab deformation in steps. here, we move ne nodes a the first step
# about 20% of their distance between the Slab2.0 model
disp_list = [0.2, 0.25, 1/3, 0.25, 1/3, 0.5, 1.]

for j, disp in enumerate(disp_list):

    print('\n \n Iter :' + str(j+1) + "/" + str(len(disp_list)) + '\n \n')

    bad_slab.transform('**RThetaPhi_to_XYZ')

    face1 = bad_slab.nsets['face.1'].mask()
    face2 = bad_slab.nsets['face.2'].mask()

    to_move_nodes = bad_slab.nsets['to_move_nodes']
    not_to_move_nodes = bad_slab.nsets['not_to_move_nodes']

    to_move = to_move_nodes.mask()
    not_to_move = not_to_move_nodes.mask()

    # we remove from the free slip condition the nodes from to_move and not_to_move nodes
    # (otherwise conflict between mpc and free slip)
    mix = np.logical_or(to_move, not_to_move)

    slab_slice1 = np.logical_and(to_move, face1)
    slab_slice2 = np.logical_and(to_move, face2)

    new_fs1 = np.logical_not(np.logical_and(mix, face1))*face1
    new_fs2 = np.logical_not(np.logical_and(mix, face2))*face2

    fs1 = bad_slab.nsets.add('mix', mask=mix)

    fs1 = bad_slab.nsets.add('fs1', mask=new_fs1)
    fs2 = bad_slab.nsets.add('fs2', mask=new_fs2)


    node_coords = bad_slab.nodes_coordinates()
    freeSlips = [fs1, fs2]

    file = open(DIR+'free_slip_eqs.inp', 'w')
    file.write("***equation\n")

    normals = []
    for plane in freeSlips:

        #computing the plane normal
        A,B,C = node_coords[plane.ranks()[[0, 11, 25]]]
        print('A,B,C', A, B, C)
        N = np.cross((B-A).T, (C-A).T)
        print('Norm of the plane normal', np.linalg.norm(N))
        N /= np.linalg.norm(N)
        normals.append(N)
        n1, n2, n3 = N
        print('Plane normal', n1, n2, n3)

        for node in plane.ids():
            file.write("**free  node:{rank}:U1 is  node:{rank}:U2 {alpha1}  node:{rank}:U3 {alpha2}  0.\n".format(rank=node, alpha1=-n2/n1, alpha2=-n3/n1))

    file.close()

    # creation of the dispU* files
    ranks = to_move_nodes.ranks()
    coords = bad_slab.nodes_coordinates()
    nset_coords = coords[ranks]

    bests=[]
    for node in nset_coords:

        dist2 = np.sum((slab_2_Hayes_XYZ-node)**2, axis=1)
        idx = np.argpartition(dist2, 3)  # idx[:3] will be the indexes of the three lowest values
        triangle = slab_2_Hayes_XYZ[idx[:3]]   # the target triangle
        proj = projection.point_to_triangle(node, triangle)
        bests.append(proj)

    bests = np.array(bests)
    U = (bests - coords[ranks])*disp

    ranks_to_move = ranks
    ranks_f1 = np.argwhere(slab_slice1)
    ranks_f2 = np.argwhere(slab_slice2)

    # nodes on the face 1
    rk_list_f1 = []
    for rk in ranks_f1:
        arg = np.argwhere(ranks_to_move == rk)[0, 0]
        rk_list_f1.append(arg)

    # nodes on the face 2
    rk_list_f2 = []
    for rk in ranks_f2:
        arg = np.argwhere(ranks_to_move == rk)[0, 0]
        rk_list_f2.append(arg)

    # correction of the displacement for the slab nodes on the sides of the mesh
    for i, n in enumerate(normals):

        for j in range(U.shape[0]):

            if i == 0 and j in rk_list_f1:

                U[j] -= np.vdot(U[j], n)*n

            if i == 1 and j in rk_list_f2:

                U[j] -= np.vdot(U[j], n)*n

    np.savetxt(DIR+'U1.dat', U[:, 0])
    np.savetxt(DIR+'U2.dat', U[:, 1])
    np.savetxt(DIR+'U3.dat', U[:, 2])

    bad_slab.save(DIR+'slab_to_deform.geof')

    pb = zset.problem.Problem()
    pb.load('slab_to_deform.inp')
    pb.run()

    bad_slab = zset.Mesh(DIR+'slab_to_deform.geof')
    bad_slab.transform('**deform_mesh *input_problem slab_to_deform.ut *magnitude 1. **classical_renumbering ')
    bad_slab.transform('**XYZ_to_RThetaPhi')
    bad_slab.save(DIR+'slab_tmp1.geof')
    zset.misc.run('refine_mmg_iterative.inp', options='-m')
    bad_slab = zset.Mesh(DIR+'slab_tmp2.geof')

bad_slab.transform('**classical_renumbering')
bad_slab.transform('**rename_set *elsets  AW-ext AW  SLAB-ext   SLAB  CH-ext  CH  CL-ext CL  OC-ext OC')
#bad_slab.elsets['AW-ext'].name = 'AW'
bad_slab.save(DIR+'slab_deformed_FLAT.geof')
bad_slab.transform('**RThetaPhi_to_XYZ')
bad_slab.save(DIR+'slab_deformed_SPHE.geof')
