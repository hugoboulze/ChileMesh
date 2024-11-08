#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: garaud, boulze

Build the various horizontal planes: -4km, -54km, -70km, -200km, -270km, -670km

"""

## TO DO: reecrire en full python en incluant union.inp

import sys
from constants import xmin, xmax, ymin, ymax, z70km, z90km, z200km, z270km, z670km

scale = 2.5 ###  scale, coherent with ../05*/scale2.5.inp

tmpl = """
***geometry
**node
4 3
1 {xmin:.5e} {ymin:.5e} {z:.5e}
2 {xmax:.5e} {ymin:.5e} {z:.5e}
3 {xmax:.5e} {ymax:.5e} {z:.5e}
4 {xmin:.5e} {ymax:.5e} {z:.5e}
**element
1
1 s3d4 1 2 3 4
***group
**elset R
 1
***return
"""

# for Zcracks, the planes need to be a bit bigger than the box
xmin -= .02
ymin -= .02
xmax += .02
ymax += .02

with open("plane_04.geof", 'w') as geof:
    z = 0.999372 * scale # idem
    geof.write(tmpl.format(**locals()))

with open("plane_70.geof", 'w') as geof:
    z = 0.9890127 * scale  # z70km , mais avec l'arrondi de arrondis.inp
    geof.write(tmpl.format(**locals()))

with open("plane_54.geof", 'w') as geof:
    z = 0.9915240 * scale  # z54km , mais avec l'arrondi de arrondis.inp
    geof.write(tmpl.format(**locals()))

with open("plane_200.geof", 'w') as geof:
    z = 0.9686078 * scale  # idem
    geof.write(tmpl.format(**locals()))

with open("plane_270.geof", 'w') as geof:
    z = 0.957620 * scale  # idem
    geof.write(tmpl.format(**locals()))

with open("plane_670.geof", 'w') as geof:
    z = z670km * scale  # idem
    geof.write(tmpl.format(**locals()))
