#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:57:04 2021

@author: hugob
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal 
import matplotlib.pyplot as plot 
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
import zset
from scipy.interpolate import LinearNDInterpolator
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import sys
sys.path.append("/home/hugo/these/outils_zset/create_disp_chile-mesh_v1.0_PUBLI/")
from create_disp_files import create_disp_files
from compute_magnitude import compute_mw
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER



def XYZtollh(vec_XYZ):
    
    vec_llh = np.zeros(vec_XYZ.shape)
    
    for i,vec in enumerate(vec_XYZ):
        
        from math import acos, asin, cos, pi , degrees, copysign
        # from JDtools import Norm
        x,y,z = vec
        r = np.linalg.norm(vec)
        lati = asin (z/r)
        unsignedlongi =  acos(x/(r*cos(lati)))    # returns the positive angle, btw 0 and pi ; 
        longi = copysign(unsignedlongi,  y/(r*cos(lati))   )
        
        vec_llh[i] = [degrees(longi), degrees(lati), EarthRadius-r]
        
    
    return vec_llh


def angle(vec1, vec2):
    u2 = vec2/np.linalg.norm(vec2)
    angle = np.zeros(vec1.shape[0])
    for i,v in enumerate(vec1):

        u1 = v/np.linalg.norm(v)
        dot_product = np.dot(u1, u2)
        angle[i] = np.arccos(dot_product)
    
    return angle


EarthRadius=6371e3

mesh_path = '/home/hugo/these/outils_zset/create_disp_chile-mesh_v1.0_PUBLI/'
maule_model = mesh_path +'chile-mesh_v1.0.geo'

lon = []
lat = []
depth = []
couplage = []

areas = []


mesh = zset.Mesh(maule_model)
interface = mesh.nsets['fault_plane_B']
ranks = interface.ranks()
coords = mesh.nodes_coordinates()
interface_coords = coords[ranks]

lld = XYZtollh(interface_coords)

lon_i = lld[:,0]
lat_i = lld[:,1]
depth_i = lld[:,2]


coords_XYZ = np.genfromtxt(mesh_path+'/coords.dat')
dip_XYZ = np.genfromtxt(mesh_path+'/Tvertical.dat')
strike_XYZ = np.genfromtxt(mesh_path+'/Thorizontal.dat')

coords_llh = XYZtollh(coords_XYZ)
dip_llh = XYZtollh(dip_XYZ + coords_XYZ)
strike_llh = XYZtollh(strike_XYZ + coords_XYZ)

plt.figure()
plt.scatter(lon_i, lat_i, c=depth_i<=72e3)
plt.axis('equal')
plt.show()

dip_vec = dip_llh - coords_llh
strike_vec = strike_llh - coords_llh


cvg_angle_deg=12
cvg_angle = cvg_angle_deg*np.pi/180 
vec_cv = np.array([np.cos(cvg_angle), np.sin(cvg_angle)]) ### on glisse de 30 m mais dans la direction de la convergence
vec_EST = np.array([1,0])
angle_cv = angle(dip_vec[:,:2], vec_cv)
angle_with_E = angle(dip_vec[:,:2], vec_EST)




R0 = 100
# disp_max = 50.
# segment = [-34, -38]
# depth = [0, 72]


### SOURCE MW9
disp_max = 9.
segment =[-34, -38]
depth = [0, 72]
c_name='uniform_Mw9_R0_'+str(R0)


fort = open('disp_files/ds-ss.'+c_name, 'w')
slip = open('disp_files/'+c_name+'.dat', 'w')
node_mesh = open('node_mesh.dat', 'w')
for i in range(lon_i.shape[0]):
    node_mesh.write('{}\t{}\n'.format(lon_i[i], lat_i[i])) 

    lat_max, lat_min = segment
    depth_min, depth_max = depth
    
    COEFF_DIP    = np.cos(angle_cv[i])
    COEFF_STRIKE = -np.sin(angle_cv[i])
    

    if angle_with_E[i] - angle_cv[i] >= 0.1:
        
        COEFF_STRIKE *= -1
    
    if lat_min <= lat_i[i] < lat_max and depth_min*1e3<=depth_i[i]<=depth_max*1e3: 

        dip    = disp_max*COEFF_DIP*R0
        strike = disp_max*COEFF_STRIKE*R0
        
        fort.write('{}\t{}\t{}\n'.format(i, dip, strike)) ### il faut mettre un - car le THorizontal est oriente Nord Sud.
        slip.write('{}\t{}\t{}\n'.format(lon_i[i], lat_i[i], disp_max)) 


fort.close()
slip.close()
node_mesh.close()

create_disp_files('disp_files/ds-ss.'+c_name, Outdir='./disp_files/', disp_name=c_name)
compute_mw('disp_files/'+c_name+'.vtk')

    
