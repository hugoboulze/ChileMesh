#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:13:28 2021

@author: boulze, garaud

Check the thickness of the SLAB and CHANNEL after the deformation process

"""

# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import zset
from SumatraTools_py3 import PtXYZToLatiLongi
# =============================================================================

DIR = './'

# choose to measure the channel (CH-ext) or the slab (SLAB-ext) thickness
geom = 'CH-ext'
# geom='SLAB-ext'

mesh = zset.Mesh(DIR+'slab_deformed_FLAT.geof')
mesh.transform("**extract_surface *elset " + geom)
mesh.transform('**RThetaPhi_to_XYZ')

surf1_ids = mesh.nsets['surface_1'].ranks()
surf2_ids = mesh.nsets['surface_2'].ranks()

node_coords = mesh.nodes_coordinates()

coord_surf1 = node_coords[surf1_ids]
coord_surf2 = node_coords[surf2_ids]

thickness = np.zeros(coord_surf2.shape)

for k in range(coord_surf2.shape[0]):
    dist2 = np.sum((coord_surf1-coord_surf2[k])**2, axis=1)
    i = np.argmin(dist2)
    thick = np.sqrt(dist2[i])


    lat, lon, d = PtXYZToLatiLongi((coord_surf2[k,0], coord_surf2[k,1], coord_surf2[k,2]))

    thickness[k,0] = lon
    thickness[k,1] = lat
    thickness[k,2] = thick


thickness = thickness[thickness[:,2]>0]

mean_th = round(np.mean(thickness[:,2]),1)
med_th = round(np.median(thickness[:,2]),1)
max_th = round(np.max(thickness[:,2]),1)
min_th = round(np.min(thickness[:,2]),1)


fig = plt.figure()

fig.suptitle('Mean: {} km  -  Max: {} km  -  Min: {} km'.format(mean_th, max_th, min_th), fontsize=25)
ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.OCEAN)
ax1.add_feature(cfeature.COASTLINE, linewidth=2)
c = ax1.scatter(thickness[:,0], thickness[:,1], c=thickness[:,2], s=20)
ax1.set_xticks([-80, -70, -60])# ax1.set_xticks(-90, -30)
ax1.set_yticks([-60, -50, -40, -30, -20, -10, 0])
ax1.set_ylabel('Latitude')
ax1.set_xlabel('Longitude')
fig.colorbar(c, label='Thickness [km]')

#histogram
ax2 = fig.add_subplot(1, 2, 2)
ax2.hist(thickness[:,2], bins=100)
ax2.set_xlabel('Thickness [km]')
ax2.set_ylabel('Number of nodes')
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_ticks_position('right')
