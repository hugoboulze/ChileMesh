#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: boulze, garaud

Disconnect oceanic and continental lithospheres

"""

# =============================================================================
import numpy as np
import zset
# =============================================================================

m = zset.Mesh('./mesh_lithospheres_to_disconnect.geo')

to_remove = ~m.elsets['LITHO_TO_DISCONNECT'].mask() # ~ means inverse of the table
m.elsets.add("REMOVEME", mask=to_remove)
m.transform('**delete_elset REMOVEME')

m.transform('**mesh_connectivity_by_face')
print(m.elsets)

ids0 = m.elsets['ELSET_0'].ids()
ids1 = m.elsets['ELSET_1'].ids()

coords = m.ip_coordinates()

# disconnection
# a trick to automatically detect which part is oceanic or continental (because the reassign of ELSET_0 and ELSET_1 is not stable)
mean_coord0 = np.mean(coords[m.elsets['ELSET_0'].ip_mask()],axis=0)[1]
mean_coord1 = np.mean(coords[m.elsets['ELSET_1'].ip_mask()], axis=0)[1]

mm = zset.Mesh('./mesh_lithospheres_to_disconnect.geo')

if mean_coord0 > mean_coord1: #oceanic part is the one with the lower mean y
	mm.elsets.add("LITHO_OCEAN_tmp", ids=ids1)
else:
	mm.elsets.add("LITHO_OCEAN_tmp", ids=ids0)

mm.save('./mesh_lithospheres_disconnected.geo')
