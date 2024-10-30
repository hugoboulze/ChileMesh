#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 17:41:27 2021

@author: boulze, garaud

Create the surface slab as a csv file.
Interpole the surface of the slab in Patagonia.

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
    Parameters
    ----------
    raw_slab : TYPE
        DESCRIPTION.
    area : list
        [long_min,long_max,lat_min,lat_max]

    step=0.05 par defaut

    Returns
    -------
    None.

    '''

    raw_slab = np.genfromtxt('./sam_slab2_dep_02.23.18.xyz', delimiter=',', dtype=float)

    depth_grid = raw_slab[:,2]
    depth_grid = np.reshape(depth_grid , (1281,581))

    return depth_grid


def extract_slab(grid_slab, lon_min, lon_max, lat_min, lat_max, max_depth, res, start_with_trench=False):
    
    '''
    Parameters
    ----------
    grid_slab : TYPE
        DESCRIPTION.
    lon_min : TYPE
        DESCRIPTION.
    lon_max : TYPE
        DESCRIPTION.
    lat_min : TYPE
        DESCRIPTION.
    lat_max : TYPE
        DESCRIPTION.
    max_depth : TYPE
        DESCRIPTION.
    res : TYPE
        DESCRIPTION.
    start_with_trench : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''


    lon_0 = 274
    lat_0 = 15
    grid_res = 0.05

    step = np.int64(res/grid_res)

    LAT_SLAB = []
    LON_SLAB = []
    DEPTH_SLAB = []


    #we search in the grid, the i and j indexes of each point of the trench
    file = open(DIR+'extracted_slab.dat','w')
    for i in range(0,grid_slab.shape[0], step):
        # print('step', step)
        lat = lat_0 - grid_res*i
        # print(lat)
        for j in range(0,grid_slab.shape[1], step):
            lon = lon_0 + grid_res*j

            if np.isnan(grid_slab[i,j]):
                continue

            else:
                if lat_min <= lat <= lat_max and lon_min <= lon-360 <= lon_max and grid_slab[i,j]>=max_depth:
                    file.write('{} {} {}\n'.format(round(lon-360,4), round(lat,4), round(grid_slab[i,j],4)))
                    LAT_SLAB.append(round(lat,4))
                    LON_SLAB.append(round(lon-360,4))
                    DEPTH_SLAB.append(round(grid_slab[i,j],4))
    file.close()

    return np.array(LON_SLAB), np.array(LAT_SLAB), np.array(DEPTH_SLAB)


def extract_slabv2(grid_slab, lon_min, lon_max, lat_min, lat_max, max_depth, res, start_with_trench=False, plot=False):
    
    '''
    Parameters
    ----------
    raw_slab : TYPE
        DESCRIPTION.
    area : list
        [long_min,long_max,lat_min,lat_max]

    step=0.05 par defaut

    Returns
    -------
    None.

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

    Parameters
    ----------
    grid_slab : TYPE
        DESCRIPTION.
    lon_min : TYPE
        DESCRIPTION.
    lon_max : TYPE
        DESCRIPTION.
    lat_min : TYPE
        DESCRIPTION.
    lat_max : TYPE
        DESCRIPTION.
    res : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    recupere les points de la grille où slab 2.0 n'existe pas et où on souhaite donc obtenir une valeur par interpolation

    '''

    lon_0 = -86
    lat_0 = 15
    grid_step = 0.05


    step = np.int(res/grid_step)
    print('step', step)

    # j = longitude
    j_min = int((np.abs(lon_0 - lon_min))/0.05)
    j_max = int((np.abs(lon_0 - lon_max))/0.05)
    #i = latitude (attention max et min inverse par rapport a longitude!!)
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

def obs_interp(slab_filtered):
    '''
    Parameters
    ----------
    slab_filtered : TYPE
        DESCRIPTION.

    Returns
    -------
    x_obs : TYPE
        DESCRIPTION.
    y_obs : TYPE
        DESCRIPTION.
    z_obs : TYPE
        DESCRIPTION.

    utilise les points x_obs, y_obs et z_obs pour construite le modèle d'interpolation
    ie, ce sont les (certains) points de slab 2.0

    '''

    slab = np.genfromtxt(slab_filtered)
    print(slab)

    x_obs = []
    y_obs = []
    z_obs = []
    file = open(DIR+'model_interpolation.dat','w')
    for i in range(slab.shape[0]):

        if slab[i][1] <= - 38:
            file.write(str(slab[i][0])+'\t'+str(slab[i][1])+'\t'+str(slab[i][2])+'\n')
            x_obs.append(slab[i][0])
            y_obs.append(slab[i][1])
            z_obs.append(slab[i][2])


    x_obs = np.array(x_obs)
    y_obs = np.array(y_obs)
    z_obs = np.array(z_obs)

    file.close()

    return x_obs, y_obs, z_obs



def slab_lld_to_XYZ(slab, res, outname):
    '''
    

    Parameters
    ----------
    slab : TYPE
        DESCRIPTION.
    res : TYPE
        DESCRIPTION.
    outname : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''

    outfile =  open(outname,'w')
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
    

    Parameters
    ----------
    slab_grid : TYPE
        DESCRIPTION.
    save : TYPE, optional
        DESCRIPTION. The default is False.
    saveName : TYPE, optional
        DESCRIPTION. The default is 'trenchFROMslab.dat'.

    Returns
    -------
    lati : TYPE
        DESCRIPTION.
    longi : TYPE
        DESCRIPTION.
    prof : TYPE
        DESCRIPTION.

    on extrait la ligne de fosse du slab filtre et interpole

    '''
    
    slab = np.genfromtxt(slab_grid)
    lat = np.unique(slab[:,1])

    lati = []
    longi = []
    prof = []
    if save:
        file = open(saveName,'w')
    for l in lat:
        args = np.argwhere(slab[:,1] == round(l,4))
        if args.shape[0] != 0:

            pt = slab[args][0][0]

            lon, lat, depth = pt[0], pt[1], pt[2]

            lati.append(lat)
            longi.append(lon)
            prof.append(depth)
            if save:
                file.write('{} {} {}\n'.format(lon, lat, depth))

    if save:
        file.close()
    
    if plot:
        plt.figure()
        plt.title('Trench from slab model')
        plt.scatter(longi, lati, c=prof)
        plt.axis('equal')
        plt.colorbar()

    print('MAX DEPTH : ', max(prof) )
    print('MIN DEPTH : ', min(prof))

    return lati, longi, prof


if __name__ == '__main__':

    # # 1. On passe le slab  sous forme de grille python
    grid_slab = xyz_to_grid('./sam_slab2_dep_02.23.18.xyz')
    # 2. On selectionne dans cette grille la region d'interet et on enregistre un fichier .dat les points correspondant
    max_depth = -500

    # extract_slabv2(grid_slab,-85,-55,-45,-5, max_depth, 0.1)
    # LON_SLAB_interp, LAT_SLAB_interp, DEPTH_SLAB_interp = extract_slabv2(grid_slab,-85,-55,-45,-5, max_depth, res_interp)
    LON_SLAB, LAT_SLAB, DEPTH_SLAB = extract_slabv2(grid_slab, -85, -55, -45, -5, max_depth, 0.1)

    LON_SLAB2, LAT_SLAB2, DEPTH_SLAB2 = extract_slabv2(grid_slab, -85, -55, -45, -5, max_depth, 0.05)
    ### on save slab2.0 avant de faire quoique ce soit pour le visualiser
    SLAB2 = np.zeros((LON_SLAB2.shape[0], 3))
    SLAB2[:, 0] = LON_SLAB2
    SLAB2[:, 1] = LAT_SLAB2
    SLAB2[:, 2] = DEPTH_SLAB2
    np.savetxt(DIR+'slabHayes_0.05deg_llh.dat', SLAB2) #===> on save slab2.0 pour le visualiser sous pv
    trench_from_slab(DIR+'./slabHayes_0.05deg_llh.dat', save=True, saveName=DIR+'trenchHayes_0.05deg_llh.dat')
    slab_lld_to_XYZ(np.genfromtxt(DIR+'trenchHayes_0.05deg_llh.dat'), 0.05, outname=DIR+'trenchHayes_0.05deg_SPHE.csv')
    slab_lld_to_XYZ(np.genfromtxt(DIR+'slabHayes_0.05deg_llh.dat'), 0.05 , outname=DIR+'slabHayes_0.05deg_SPHE.csv')

    ### on construit la nouvelle trench
    trenchGMT = np.genfromtxt('trench_Chile.gmt', comments='>')
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
    slab_lld_to_XYZ(trench, 0.05 , outname=DIR+'trench_Hayes_and_GMT_SPHE.csv')

    lon_trench = trench[:, 0]
    lat_trench = trench[:, 1]


    # LATITUDE A LAQUELLE ON COUPE SLAB2.0 ==> ON VA INTERPOLER EN DESSOUS CAR ABSENCE DE SLAB
    lat_coupure = -44.
    lat_copy = -44.

    LON_SLAB_part1 = LON_SLAB[LAT_SLAB >= -40]
    DEPTH_SLAB_part1 = DEPTH_SLAB[LAT_SLAB >= -40]
    LAT_SLAB_part1 = LAT_SLAB[LAT_SLAB >= -40]

    LON_TRAIN = np.array([])
    LAT_TRAIN   = np.array([])
    DEPTH_TRAIN   = np.array([])

    x_40deg = LON_SLAB[LAT_SLAB == -40]
    z_40deg = DEPTH_SLAB[LAT_SLAB == -40]

    for lat in np.arange(lat_coupure-0.1, -55, -1.):

        lat = round(lat, 1)

        ### on copie la derniere ligne a lat fixe du slab connue
        x_lat = LON_SLAB[LAT_SLAB == lat_copy]
        z_lat = DEPTH_SLAB[LAT_SLAB == lat_copy]

        val_trench = lon_trench[np.argmin(np.abs(lat_trench - lat))]

        ### on copie colle des profils le long de la fosse et on ramene les profils copie colle a la fosse
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

    LON_EVAL = np.array([])
    LAT_EVAL = np.array([])
    DEPTH_EVAL = np.array([])

    for lat in np.arange(-40.1, -55, -0.1):

        lat = round(lat,1)
        x_lat = LON_SLAB[LAT_SLAB == -40]
        val_trench = lon_trench[np.argmin(np.abs(lat_trench - lat))]

        ### on copie colle des profils le long de la fosse et on ramene les profils copie colle a la fosse
        x_lat -= x_lat[0] - val_trench

        y_lat = lat*np.ones(x_lat.shape[0])

        LON_EVAL  = np.concatenate((LON_EVAL, x_lat))
        LAT_EVAL  = np.concatenate((LAT_EVAL, y_lat))

    #on a besoin pour l interpolation de coller la partie du slab au nord
    LON_SLAB, LAT_SLAB, DEPTH_SLAB = extract_slabv2(grid_slab, -85, -55, -45, -5, max_depth, 0.5)
    ### on sauve la table pour l interpolation
    train = np.zeros((LON_TRAIN.shape[0] + LON_SLAB.shape[0], 3))
    train[:, 0] =  np.concatenate((LON_TRAIN, LON_SLAB))
    train[:, 1] =  np.concatenate((LAT_TRAIN, LAT_SLAB))
    train[:, 2] =  np.concatenate((DEPTH_TRAIN, DEPTH_SLAB))
    np.savetxt(DIR+'train.dat', train)

    ### on sauve la table de points a interpoler
    evaluate = np.zeros((LON_EVAL.shape[0], 2))
    evaluate[:, 0] =  LON_EVAL
    evaluate[:, 1] =  LAT_EVAL
    np.savetxt(DIR+'evaluate.dat', evaluate)

    #on interpole la grille 0.5deg avec gmt et on evalue sur celle a 0.1deg
    os.system('bash interpolation.sh')

    eval_slab = np.genfromtxt(DIR+'evaluate_slab.dat')
    LON_TO_ADD = eval_slab[:, 0]
    LAT_TO_ADD = eval_slab[:, 1]
    DEPTH_TO_ADD = eval_slab[:, 2]

    LON_FINAL = np.concatenate((LON_SLAB_part1, LON_TO_ADD))
    LAT_FINAL = np.concatenate((LAT_SLAB_part1, LAT_TO_ADD))
    DEPTH_FINAL =  np.concatenate((DEPTH_SLAB_part1, DEPTH_TO_ADD))

    #conversion au format zebulon XYZ
    slab = np.zeros((LON_FINAL.shape[0], 3))
    slab[:, 0] = LON_FINAL #+0.05
    slab[:, 1] = LAT_FINAL
    slab[:, 2] = DEPTH_FINAL

    np.savetxt(DIR+'slabSurf_0.1deg_llh.csv', slab)

    slab_lld_to_XYZ(slab, 0.1, outname=DIR+'slabSurf_0.1deg_SPHE.csv')

  
    # plot
    
    # fig, ax = plt.subplots(1, 1, subplot_kw={"projection": ccrs.PlateCarree()})

    # # ax.add_feature(cfeature.LAND,color="lightgrey")
    # ax.coastlines(resolution='10m', color='black', linewidth=1)

    # ax.scatter(slab[:, 0], slab[:, 1], c=slab[:, 2])
    # ax.plot(trench[:, 0], trench[:, 1], c='k')
    # plt.tight_layout()
    # plt.show()
