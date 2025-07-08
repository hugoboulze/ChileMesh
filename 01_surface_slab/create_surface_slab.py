#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 17:41:27 2021

@author: boulze, garaud

Create the surface slab as a csv file.
Extrapole the surface of the slab in Patagonia.

"""

# =============================================================================
import os
import sys
sys.path.append('./../..')
import numpy as np
import matplotlib.pyplot as plt
from tools import PtLatiLongiToXYZ
# =============================================================================

DIR = './'

def xyz_to_grid(raw_slab):

    '''
    raw_slab: sam_slab2_dep_02.23.18.xyz
    area : list
        [long_min,long_max,lat_min,lat_max]

    step=0.05 par defaut

    Returns
    -------
    None.

    '''

    raw_slab = np.genfromtxt(raw_slab, delimiter=',', dtype=float)

    depth_grid = raw_slab[:,2]
    depth_grid = np.reshape(depth_grid , (1281,581))

    return depth_grid


def extract_slab(grid_slab, lon_min, lon_max, lat_min, lat_max, max_depth, res, start_with_trench=False, plot=False):
    
    '''
    extract a piece of the slab in the grid according to lon_min/max, lat_min/max,  max_depth and res
    
    grid_slab: = [[lon_i, lat_i, depth_i], ...]
    step = 0.05 by default in Slab2.0

    '''

    lon_0 = 274
    lat_0 = 15


    grid_res = 0.05

    step = np.int64(res/grid_res)

    LAT_SLAB = []
    LON_SLAB = []
    DEPTH_SLAB = []

    #on parcourt la grille en latitudes
    for i in np.arange(0, grid_slab.shape[0], step):

        lat = lat_0 - grid_res*i

        #quand la latitude est bonne on prend la premiere valeur non 'nan' en longitude de maniere a recup la fosse
        if lat_min <= lat <= lat_max:

            for j in np.arange(0, grid_slab.shape[1], 1):

                # print(grid_slab[i,j])
                if not np.isnan(grid_slab[i,j]):
                    # start_lon = lon_0 + j*grid_res
                    start_lon_idx = j
                    break

            for l in range(start_lon_idx, grid_slab.shape[1], step):

                if not np.isnan(grid_slab[i,l]):

                    lon = lon_0 + l*grid_res

                    LAT_SLAB.append(round(lat,4))
                    LON_SLAB.append(round(lon-360,4))
                    DEPTH_SLAB.append(round(grid_slab[i,l],4))

    if plot:
        plt.figure()
        plt.axis('equal')
        plt.xlabel('Longitude [deg]')
        plt.ylabel('Latitude [deg]')
        plt.scatter(LON_SLAB, LAT_SLAB, c=DEPTH_SLAB)
        plt.show()
    

    return np.array(LON_SLAB), np.array(LAT_SLAB), np.array(DEPTH_SLAB)




def extract_interp(grid_slab,lon_min, lon_max, lat_min, lat_max, res):
    
    '''
    retrieve points from Slab2.0 grid where the slab is not defined
    and where we want to get interpolation value

    '''

    lon_0 = -86
    lat_0 = 15
    grid_step = 0.05


    step = np.int(res/grid_step)
    # print('step', step)

    # j = longitude
    j_min = int((np.abs(lon_0 - lon_min))/0.05)
    j_max = int((np.abs(lon_0 - lon_max))/0.05)
    #i = latitude (careful: max and min are in contrary sense with respect to longitude
    i_max = int((np.abs(lat_0 - lat_min))/0.05)
    i_min = int((np.abs(lat_0 - lat_max))/0.05)

    extracted_grid = grid_slab[i_min:i_max+1,j_min:j_max+1]

    x_int = []
    y_int = []

    lat_0 = lat_max
    lon_0 = lon_min

    file = open(DIR+'to_interpolate.dat','w')

    for i in range(0,extracted_grid.shape[0], step):
        lat = lat_0 - grid_step*i
        for j in range(0,extracted_grid.shape[1], step):
            lon = lon_0 + grid_step*j
            if np.isnan(extracted_grid[i,j]):
                x_int.append(lon)
                y_int.append(lat)
                file.write(str(lon) + '\t' + str(lat)+'\n')

    file.close()
    return np.array(x_int), np.array(y_int)


def slab_lld_to_XYZ(slab, outname):
    
    '''
    slab: [[lon_i, lat_i, depth_i], .... ]
    outname: file of the slab in XYZ coordinates
    '''

    outfile = open(outname,'w')
    i = 0

    ret = ""
    for line in slab:
        i = i+1

        lon = line[0]
        lat = line[1]

        if line.shape[0] == 3:
            depth = -line[2]
        else:
            depth = 0

        X,Y,Z = PtLatiLongiToXYZ([lat,lon], depth) # passage de km en m (en fait ca depend de l'unite du rayon de la terre dans les scripts de JD)
        ret += "%3d   "%i + "%.10e %.10e %.10e"%tuple((X,Y,Z))+"\n"
        outfile.write('{},{},{}\n'.format(X, Y, Z))

    outfile.close()


def trench_from_slab(slab_grid, save=False, saveName='trenchFROMslab.dat', plot=False):
    
    '''
    extract the trench path from the given slab grid: i.e. at a given depth the shallower points

    '''
    
    slab = np.genfromtxt(slab_grid)
    lat = np.unique(slab[:,1])

    lati = []
    loni = []
    depthi = []
    if save:
        file = open(saveName,'w')
    for l in lat:
        args = np.argwhere(slab[:,1] == round(l,4))
        if args.shape[0] != 0:

            pt = slab[args][0][0]

            lon, lat, depth = pt[0], pt[1], pt[2]

            lati.append(lat)
            loni.append(lon)
            depthi.append(depth)
            if save:
                file.write('{} {} {}\n'.format(lon, lat, depth))

    if save:
        file.close()
    
    if plot:
        plt.figure()
        plt.title('Trench from slab model')
        plt.scatter(loni, lati, c=depthi)
        plt.axis('equal')
        plt.colorbar()

    print('MAX DEPTH : ', max(depthi))
    print('MIN DEPTH : ', min(depthi))

    return lati, loni, depthi


if __name__ == '__main__':
    
    max_depth = -500 # in km.
    
    # reading slab2.0 and creating python grid
    grid_slab = xyz_to_grid('./sam_slab2_dep_02.23.18.xyz')
    
    # save slab2.0 if comparisons needed
    LON_SLAB2, LAT_SLAB2, DEPTH_SLAB2 = extract_slab(grid_slab, -85, -55, -45, -5, max_depth, 0.05)
    SLAB2 = np.zeros((LON_SLAB2.shape[0], 3))
    SLAB2[:, 0] = LON_SLAB2
    SLAB2[:, 1] = LAT_SLAB2
    SLAB2[:, 2] = DEPTH_SLAB2
    np.savetxt(DIR+'slabHayes_0.05deg_llh.dat', SLAB2)
    
    trench_from_slab(DIR+'./slabHayes_0.05deg_llh.dat', save=True, saveName=DIR+'trenchHayes_0.05deg_llh.dat')
    # convert in X,Y,Z the trench from Slab2.0 (shallower points), in csv easier to plot with Paraview (Table to Points filter)
    slab_lld_to_XYZ(np.genfromtxt(DIR+'trenchHayes_0.05deg_llh.dat'), outname=DIR+'trenchHayes_0.05deg_SPHE.csv')
    # convert in X,Y,Z the slab grid, in csv easier to plot with Paraview (Table to Points filter)
    slab_lld_to_XYZ(np.genfromtxt(DIR+'slabHayes_0.05deg_llh.dat'), outname=DIR+'slabHayes_0.05deg_SPHE.csv')
    
    
    # extract a point every 0.1° in Slab2.0 (points every 0.05°)
    LON_SLAB, LAT_SLAB, DEPTH_SLAB = extract_slab(grid_slab, -85, -55, -45, -5, max_depth, 0.1)

    
    # =============================================================================
    #     TRENCH OPERATIONS
    # =============================================================================
    
    # building the new trench: mix between GMT trench and the trench in Slab2.0 (shallower points of Slab2.0)
    trenchGMT = np.genfromtxt(DIR+'trench_Chile.gmt', comments='>')
    trenchHayes = np.genfromtxt(DIR+'trenchHayes_0.05deg_llh.dat')[:, :2]

    argsHayes = np.argwhere(trenchHayes[:,1] >= -44.2)
    argsGMT = np.argwhere(trenchGMT[:,1] < -44.2)

    argsHayes = argsHayes.reshape(argsHayes.shape[0],)
    argsGMT = argsGMT.reshape(argsGMT.shape[0],)

    trenchHayes = trenchHayes[argsHayes]
    trenchGMT = trenchGMT[argsGMT]

    trench = np.zeros((trenchHayes.shape[0]+trenchGMT.shape[0],2))
    trench[:, 0] = np.concatenate((trenchHayes[:,0], trenchGMT[:,0]))
    trench[:, 1] =  np.concatenate((trenchHayes[:,1], trenchGMT[:,1]))
    np.savetxt(DIR+'trench_Hayes_and_GMT_llh.csv',trench)
    slab_lld_to_XYZ(trench, outname=DIR+'trench_Hayes_and_GMT_SPHE.csv') #convert to X,Y,Z

    lon_trench = trench[:, 0]
    lat_trench = trench[:, 1]

    # =============================================================================
    #     EXTRAPOLATION + interpolation
    # =============================================================================
    
    lat_end = -44. #latitude from which to the South we create synthetic profiles

    # we retrieve all the points northern to 40°S
    LON_SLAB_part1 = LON_SLAB[LAT_SLAB >= -40]
    DEPTH_SLAB_part1 = DEPTH_SLAB[LAT_SLAB >= -40]
    LAT_SLAB_part1 = LAT_SLAB[LAT_SLAB >= -40]
    
    # points to keep to create the interpolation grid (training points)
    LON_TRAIN = np.array([])
    LAT_TRAIN   = np.array([])
    DEPTH_TRAIN   = np.array([])

    # last latitude at which a profile of the slab is fully defined: we copy this profile between 44°S to 55°S
    lat_copy = -40
    x_40deg = LON_SLAB[LAT_SLAB == lat_copy]
    z_40deg = DEPTH_SLAB[LAT_SLAB == lat_copy]

    for lat in np.arange(lat_end - 0.1, -55, -1.):

        lat = round(lat, 1)

        # last defined latitude in Slab2.0
        x_lat = LON_SLAB[LAT_SLAB == lat_end]
        z_lat = DEPTH_SLAB[LAT_SLAB == lat_end]

        # calculate the gap between the actual westward longitude of the profile and the trench longitude at a given latitude (lat index)
        val_trench = lon_trench[np.argmin(np.abs(lat_trench - lat))]
        
        #copy/paste profiles along the trench, and we ensure that the begining of the profile is at the trench
        x_lat -= x_lat[0] - val_trench

        x_latp2 = x_40deg[x_40deg > x_lat[-1]]
        z_latp2 = z_40deg[x_40deg > x_lat[-1]]

        z_latp2 -= np.abs(z_lat[-1] - z_latp2[0])
        x_latp2 -= np.abs(x_lat[-1] - x_latp2[0])

        x_lat = np.concatenate((x_lat, x_latp2[0:]))
        z_lat = np.concatenate((z_lat, z_latp2[0:]))

        y_lat = lat*np.ones(x_lat.shape[0])

        LON_TRAIN = np.concatenate((LON_TRAIN, x_lat))
        LAT_TRAIN = np.concatenate((LAT_TRAIN, y_lat))
        DEPTH_TRAIN = np.concatenate((DEPTH_TRAIN, z_lat))


    # evaluation of the slab interpolation along a 0.1° grid from 40.1°S to 55°S
    LON_EVAL = np.array([])
    LAT_EVAL = np.array([])
    DEPTH_EVAL = np.array([])
    
    # for each latitude we create a profile in longitude the same length as 40°S from 40°1S to 55°S
    for lat in np.arange(-40.1, -55, -0.1):

        lat = round(lat,1)
        x_lat = LON_SLAB[LAT_SLAB == -40]
        val_trench = lon_trench[np.argmin(np.abs(lat_trench - lat))]

        #copy/paste profiles along the trench, and we ensure that the begining of the profile is at the trench
        x_lat -= x_lat[0] - val_trench

        y_lat = lat*np.ones(x_lat.shape[0])

        LON_EVAL  = np.concatenate((LON_EVAL, x_lat))
        LAT_EVAL  = np.concatenate((LAT_EVAL, y_lat))

    # for interpolation, need to paste the north part of the slab to the south to avoid border effects
    LON_SLAB, LAT_SLAB, DEPTH_SLAB = extract_slab(grid_slab, -85, -55, -45, -5, max_depth, 0.5)
    

    # save data points for interpolation
    train = np.zeros((LON_TRAIN.shape[0] + LON_SLAB.shape[0], 3))
    train[:, 0] =  np.concatenate((LON_TRAIN, LON_SLAB))
    train[:, 1] =  np.concatenate((LAT_TRAIN, LAT_SLAB))
    train[:, 2] =  np.concatenate((DEPTH_TRAIN, DEPTH_SLAB))
    np.savetxt(DIR+'train.dat', train)
    # slab_lld_to_XYZ(train, outname=DIR+'train_SPHE.csv') #uncomment to visualize the result with Paraview
    
    # save the points where interpolation is needed
    evaluate = np.zeros((LON_EVAL.shape[0], 2))
    evaluate[:, 0] =  LON_EVAL
    evaluate[:, 1] =  LAT_EVAL
    np.savetxt(DIR+'evaluate.dat', evaluate)
    # slab_lld_to_XYZ(evaluate, outname=DIR+'eval_SPHE.csv') #uncomment to visualize the result with Paraview
    
    # interpolation at EVAL points using GMT: interpolation og the 0.5deg grid, and evaluation on a 0.1deg grid
    os.system('bash interpolation.sh') # outfile: evaluate_slab.dat

    #we retrieve the 
    eval_slab = np.genfromtxt(DIR+'evaluate_slab.dat')
    LON_TO_ADD = eval_slab[:, 0]
    LAT_TO_ADD = eval_slab[:, 1]
    DEPTH_TO_ADD = eval_slab[:, 2]

    # =============================================================================
    #     CONVERSION + final save
    # =============================================================================

    LON_FINAL = np.concatenate((LON_SLAB_part1, LON_TO_ADD))
    LAT_FINAL = np.concatenate((LAT_SLAB_part1, LAT_TO_ADD))
    DEPTH_FINAL =  np.concatenate((DEPTH_SLAB_part1, DEPTH_TO_ADD))

    #creation of the numpy final grid llh for conversion in X,Y,Z coordinates
    slab = np.zeros((LON_FINAL.shape[0], 3))
    slab[:, 0] = LON_FINAL #+0.05
    slab[:, 1] = LAT_FINAL
    slab[:, 2] = DEPTH_FINAL

    # we save the grid in llh format (e.g. for plots)
    np.savetxt(DIR+'slabSurf_0.1deg_llh.csv', slab)

    # convert to spherical coordinates (X,Y,Z)
    slab_lld_to_XYZ(slab, outname=DIR+'slabSurf_0.1deg_SPHE.csv')