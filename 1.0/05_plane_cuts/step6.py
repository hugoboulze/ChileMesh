#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: boulze, garaud

Create the 2 edges for north and south planes

"""

# =============================================================================
import sys
import numpy as np
import zset
sys.path.append('./../../../')
from constants import z400km
# =============================================================================


m = zset.Mesh('mesh-before-cut-NordSud.geo')

m.transform("**nset SLAB *use_elset SLAB *function 1.;")

slab = m.nsets['SLAB']
x,y,z = m.nodes_coordinates()[slab.mask()].T

# edge south is easy, it has the smaller y
ymin = np.min(y)
m.transform(f"**nset EDGE_SOUTH *use_elset SLAB *function (y-{ymin} < 1.e-4);")
edge_south = m.nsets['EDGE_SOUTH']
c0 = m.nodes_coordinates()[edge_south.ranks()[0]]
print(c0)
m.transform(f"**function *nset EDGE_SOUTH *xtrans {c0[0]}; *ytrans {c0[1]}; ")

# edge north is also simple, it has the minimal x+y:
mini = np.argmin(x+y)
xmini = x[mini]
ymini = y[mini]
m.transform(f"**nset EDGE_NORTH *use_elset SLAB *function sqrt( (x-({xmini})) ^2 + (y-({ymini}))^2 ) < 1.e-4;")
edge_north = m.nsets['EDGE_NORTH']
c1 = m.nodes_coordinates()[edge_north.ranks()[0]]
print(c1)
m.transform(f"**function *nset EDGE_NORTH *xtrans {c1[0]}; *ytrans {c1[1]}; ")

tmpl = open("north_south_planes.geof.tmpl").read()
tmpl2 = tmpl.format(c00=c0[0], c01=c0[1], c10=c1[0], c11=c1[1], zmin=z400km*2.5)
open("plans-nord-sud.geof", 'w').write(tmpl2)
print("Wrote plans-nord-sud.geof")
print("Please check above that EDGE_NORTH and EDGE_SOUTH have a few (6) nodes.")


m.transform("**check_quality")

m.save('mesh-before-cut-NordSud.geo')

assert len(m.nsets['EDGE_SOUTH']) >2 and len(m.nsets['EDGE_SOUTH']) <10, "EDGE_SOUTH is expected to have ~6 nodes, not %d. Check the mesh!"%len(m.nsets['EDGE_SOUTH'])
assert len(m.nsets['EDGE_NORTH']) >2 and len(m.nsets['EDGE_NORTH']) <10, "EDGE_NORTH is expected to have ~6 nodes, not %d. Check the mesh!"%len(m.nsets['EDGE_NORTH'])
