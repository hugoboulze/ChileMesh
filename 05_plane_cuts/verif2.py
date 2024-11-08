import numpy as np
import functools
from zset import Mesh, Serializer, Problem

"""
Verification between `Zrun -m step2` and `Zrun -zp zcrack2.z7p`.
"""

before = Mesh('mesh-before-knife1.geo')

# check CUT_ME is ok
a = len(before.elsets['ALL'])
b = len(before.elsets['CUT_ME'])
b = len(before.elsets['CUT_ME'])
c = len(before.elsets['SLAB'])
d = len(before.elsets['AW'])

assert a == b+c+d, "ALL is not equal to CUT_ME + SLAB + AW"


# check cut planes are scaled properly:
zcoords = before.nodes_coordinates()[:,2]
zplanes = Mesh('planes_200_270.geof').nodes_coordinates()[:,2]

assert np.min(zcoords) < np.min(zplanes), "Cut plane is below the box ?!"
assert np.max(zcoords) > np.max(zplanes), "Cut plane is above the box ?!"

# building the Problem is a little long, let's do it only once.
pb1 = Problem(type='math')
pb1.attach_mesh(before)
pb1.initialize()

def vol(elset, pb):
    vols = Serializer('element_volume', pb, where=elset).serialize()
    v = np.sum(vols)
    #print(f"vol({elset}) = {v}")
    return v

pb2 = Problem(type='math')
pb2.attach_mesh(Mesh('mesh_knifed_200_270.geo'))
pb2.initialize()

vol1 = functools.partial(vol, pb=pb1)
vol2 = functools.partial(vol, pb=pb2)

print(vol1('SLAB'), vol1('AW'), vol1('CH'), vol1('COMP'))
print(vol2('SLAB'), vol2('AW'), vol2('CH'), vol2('COMP'))

#TODO:could assert
# - that |vol1-vol2| < epsilon(1.e-4) ?
# - that sum(vol1) == sum(vol2) == l*L*h
