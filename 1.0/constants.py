#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 12:00:48 2024

@author: boulze, garaud

Constant values used during the mesh building processing

"""

# =============================================================================
import numpy as np
# =============================================================================

# mean radius of the Earth
earth_radius_km = 6371.
earth_radius_m = earth_radius_km*1e3


# some basics function but useful =============================================


def Za(altitude):
    return altitude/earth_radius_km


def Zp(depth):
    return (earth_radius_km - depth)/earth_radius_km


def make_Zs(tab):
    for z in tab:
        print("z{}km = {}".format(z, Zp(z)))


def d2r(x):
    """
    Degree to radian
    """
    return np.pi*x/180.

# =============================================================================
#                           mesh bounding box area
#                   here chosen to cover the South-American continent
# x: lat in rad
# y: lon in rad
# =============================================================================


xmin = d2r(-60)
xmax = d2r(13)
ymin = d2r(-105)
ymax = d2r(-20)

# =============================================================================
# depth values for 3D flat geometry
# =============================================================================

zmax = 1.0
z4km = 0.9993721550776958  # i.e. Zp(4)
z54km = 0.9915240935488934
z70km = 0.9890127138596767
z90km = 0.9858734892481557
z100km = 0.9843038769423952
z150km = 0.9764558154135928
z200km = 0.9686077538847905
z270km = 0.9576204677444671
z400km = 0.937215507769581
z670km = 0.894835975514048
z2900km = 0.5448124313294617  # Mantle Core boundary
zmin = z2900km
