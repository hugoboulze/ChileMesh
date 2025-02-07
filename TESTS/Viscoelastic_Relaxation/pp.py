#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:57:04 2021

@author: jean-didier garaud, hugo boulze

Convert the .vtk file from the Zset post-processing into time-series of displacements at required locations

"""
import os
import numpy as np
import shutil


def xyz_to_ENup(pt, disp):
    """
    from disp in XYZ coordinates in ENU
    """

    nrm = np.linalg.norm(pt)
    U = pt/nrm
    E = np.cross(np.array([0.,0.,1.]),U)
    nrm = np.linalg.norm(E) 
    E = E/nrm 
    N = np.cross(U, E)

    dE = np.dot(E,disp)
    dN = np.dot(N,disp)
    dU = np.dot(U,disp)

    return (dE, dN, dU)


def vtk_XYZ_to_dat_ENU(filename, stations):
    
    '''
    read the .vtk from the post-processing (disp in XYZ) and convert it in a readable .dat file (disp in ENU)
    '''

    Stations = np.genfromtxt(stations, dtype=str)[:,3]
    
    outname = filename.split('.vtk')[0]+'.dat'    
    fileout = open(outname, 'w')

    idx=0  #id station
    Nodes = []
    Section=None
    NumLigne=0
    
    fileout.write("#  Station      East(mm)        North(mm)     Up(mm) \n")
    
    for ligne in open(filename,'r'): 
        
        NumLigne += 1
        
        if (ligne.strip() == ""):
            continue # sinon les lignes vides passent par les maps
    
        # Reconnaissance des blocs
        if ligne.startswith("POINTS"): 
            Section = "Nodes"
            continue
        if ligne.startswith("CELLS"): 
            Section = "Elements"
            continue
        if ligne.startswith("CELL_TYPES"): 
            Section = "ElementTypes"
            continue
        if ligne.startswith("POINT_DATA"): 
            Section = "PointData"
            continue
        
        
        if Section=="Nodes": 
            try: 
                node = np.array(ligne.split()).astype(float)
                Nodes.append(node)
                continue
            
            except (ValueError):
                if len(Nodes) != Stations.shape[0] : 
                    print("Leaving Nodes at line %d: '"%NumLigne, ligne,"'")
                    print(Nodes[0], Nodes[-2], Nodes[-1])
                Section=None
    
        if Section=="PointData":
            
            if ligne.startswith("SCALARS"): 
                
                tmp=ligne.split()[1]  # Displacement@1days or Displacement@1year
                
                num=''.join(filter(lambda c: ((c>='0') & (c<='9'))|(c in ['.', '-']) , tmp)) #extract the date after the earthquake
                
                date = float(num)
                
                suffix=tmp[-5:]
                
                if suffix=="years": 
                    date *= 365.
                
                fileout.write('# time (days) %11.5f\n'%date)
                
                idx=0
                
                continue            
            
            elif ligne.startswith("LOOKUP_TABLE"):
                continue
            
            else:
                data = np.array(ligne.split()).astype(float)*1000 #passage de km en m

            E, N, U = xyz_to_ENup(Nodes[idx], data[:3])
            fileout.write('%11.5f  %e  %e  %e\n'%(date, E, N, U)) 
            idx += 1
    
    
    fileout.close()
    
    
def create_zset_time_serie(station_list, disp_file, R0, name_dir):
    
    '''
    create time-series of displacements from .dat file
    '''
    
    if os.path.exists(name_dir):
        shutil.rmtree(name_dir)
        os.mkdir(name_dir)
    else:
        os.mkdir(name_dir)
        
    station_list = np.genfromtxt(station_list, dtype=str)
    disp_file = np.genfromtxt(disp_file)

    nb_stations = station_list.shape[0]

    for cGPS in station_list:

        i = np.argwhere(station_list[:,3]==cGPS[3])
        
        dy = []
        disp = {'E': [], 'N':[], 'U':[]}
        file = open(name_dir+'/'+cGPS[3] + '.dat','w')
        file.write('#time(yr), E(mm), N(mm), U(mm)\n')
    
        block = nb_stations
        for k in range(0, disp_file.shape[0], block):
      
            dY = disp_file[k+i,0][0,0]/365. #from days to years
            dE = disp_file[k+i,1][0,0]
            dN = disp_file[k+i,2][0,0]
            dU = disp_file[k+i,3][0,0]
            
            if k!=0:
    
                dE /= R0
                dN /= R0
                dU /= R0
                
            dy.append(dY)
            disp['E'].append(dE)
            disp['N'].append(dN)
            disp['U'].append(dU)
            
            file.write('{},{},{},{}\n'.format(dY, dE, dN, dU))

        file.close()

if __name__ == '__main__':

    points_2_reloc = './reloc/grid_-80_-30_-55_0_0.5deg_XYZ.dat' #grid with points spaced by 0.5deg, extending from 80W to 30W and to 0N to 55S.
    vtk_file = 'reference_model_grid.vtk' #output from the Zrun -pp reference_model.inp, relocated displacements in XYZ
    dat_file = 'reference_model_grid.dat' #name of the intermediate file with relocated displacements in ENU
    
    R0 = 100 #to scale the displacements by a factor of 100. 
    
    vtk_XYZ_to_dat_ENU(vtk_file, points_2_reloc)
    create_zset_time_serie(points_2_reloc, dat_file, R0=R0, name_dir='tS_grid')
            
            
            
            
            
            
            
            
            
