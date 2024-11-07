#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: boulze, garaud

Create the nodesets that will me moved and keep fixed during the slab deformation.

"""

# =============================================================================
import numpy as np
import zset
# =============================================================================

DIR = './'

bad_slab = zset.Mesh(DIR+'tmp3.geof')
surface_slab_ext = bad_slab.nsets['surface_slab-ext'].mask()
base_aw_ext = bad_slab.nsets['base_aw-ext'].mask()
surface_earth1_ext = bad_slab.nsets['surface_earth1-ext'].mask()
surface_earth2_ext = bad_slab.nsets['surface_earth2-ext'].mask()
surface_ext = bad_slab.nsets['surface-ext'].mask()
surface_aw_ext = bad_slab.nsets['surface_aw-ext'].mask()
left_ext = bad_slab.nsets['left-ext'].mask()
surface_litho_oc_ext = bad_slab.nsets['surface_litho_oc-ext'].mask()
Px0y8_ext = bad_slab.nsets['Px0y8-ext'].mask()
corner_aw_ext = bad_slab.nsets['corner_aw-ext'].mask()


not_to_move_aw = np.logical_not(corner_aw_ext)*base_aw_ext
not_to_move = np.logical_or.reduce((surface_ext, surface_earth1_ext, surface_earth2_ext,
                                    surface_aw_ext, left_ext, surface_litho_oc_ext, not_to_move_aw))
to_move = surface_slab_ext
to_move_nodes = bad_slab.nsets.add('to_move_nodes', mask=to_move)
not_to_move_nodes = bad_slab.nsets.add('not_to_move_nodes', mask=not_to_move)

bad_slab.save(DIR+'slab_to_refine_SPHE.geof')
