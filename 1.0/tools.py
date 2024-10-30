"""
Lots of tools for manipulating Earth related data:
- read GMT, Engdahl files
- translate them to VKT, geof, ...
- etc...
"""

__author__ = "JD Garaud"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2008/07/07 $"

EarthRadius=6371. #in km
import numpy as np

class Fault:
    "This class describes a fault (or, more generally, a list of points)"
    def __init__(self,its_name):
        "Faults sometimes have a name "
        self.name=its_name
        self.points = []       # optimisation possible : mettre un 2 ou 3 ou 4 tuple ?
    def add_point(self,point):
        "Appends a point to the fault"
        self.points.append(point)


def ReadGMT(filename):
    """Reads a GMT file, with space separated fields;
    returns the list of faults.
    Such files are created with a command like 'pscoast -R141/145/34/41 -Dl -m -W -JM1' (option -m is the key) """
    faults=[]
    try:
        gmt_file = open(filename)
        for ligne in gmt_file :
            if (ligne.strip().startswith("#") or ligne.isspace()):   # handle blank and comment lines
                pass
            elif (ligne.startswith(">")) :
                nom = ligne[1:-1]
                if (nom == "") : nom = "Unnamed"
                faults.append(Fault(nom))
            else :
                fault = faults[-1]
                s = ligne.split()
                try:
                    fault.add_point( ( float(s[0]),float(s[1])) )   # GMT file is lati/longi
                except (ValueError):
#                     print "ReadGMT warning:"
#                     print "  Unexpected value in file `%s'."%filename
#                     print "  Trying to read it with comma-separated mode."
                    gmt_file.close()
                    return ReadGMTComma(filename)
                except (IndexError):
                    if (ligne != "\n") :  # this allows empty lines
                        print("Splitting current line failed: Line read is", ligne)
        print("Reading `%s' successful"%filename)
        faults2 = CheckLatiLongi(faults)
        return faults2
    except (IOError) :
        print("Can't open", filename)
        print("Returning an empty Fault list")
        return []

def ReadGMTComma(filename):
    """Reads a GMT file, with comma separated fields;
    returns the list of faults"""
    faults=[]
    try:
        gmt_file = open(filename)
        for ligne in gmt_file :
            if (ligne[0] == ">") :
                nom = ligne[1:-1]
                if (nom == "") : nom = "Unnamed"
                faults.append(Fault(nom))
            else :
                fault = faults[-1]
                s = ligne.split(",")
                fault.add_point( ( float(s[0]),float(s[1])) )   # GMTcomma file is longi/lati ... I'll reverse later
        print("Reading `%s' successful (in csv mode)"%filename)
        faults2 = CheckLatiLongi(faults)
        return faults2
    except (IOError) :
        print("Can't open", filename)
        print("Returning an empty Fault list")
        return []


def PtLatiLongiToXYZ(pt, depth=0.):
    "Converts (latitude,longitude, [optionally depth]) point (float 2 or 3-tuple) to xyz (float 3-tuple) coordinates"
    from math import cos, sin, pi
    lati = pt[0]
    longi = pt[1]
    radius = EarthRadius - depth
    x = radius * cos(longi * pi/180.) * cos(lati * pi/180.)
    y = radius * sin(longi * pi/180.) * cos(lati * pi/180.)
    z = radius * sin(lati  * pi/180.)
    return (x,y,z)

def PtLongiLatiToXYZ(pt, depth=0.):
    longi=pt[0]
    lati=pt[1]
    return PtLatiLongiToXYZ((lati,longi), depth)

def PtXYZToLatiLongi(pt, depth=0.):
    "Converts xyz coordinates to (latitude,longitude, depth)"
    from math import acos, asin, cos, pi , degrees, copysign
    # from JDtools import Norm
    x,y,z = pt
    r = np.linalg.norm(pt)
    lati = asin (z/r)
    unsignedlongi =  acos(x/(r*cos(lati)))    # returns the positive angle, btw 0 and pi ;
    longi = copysign(unsignedlongi,  y/(r*cos(lati))   )

    return (degrees(lati),degrees(longi),EarthRadius-r)
 #   return (degrees(lati),degrees(longi),r)

def LatiLongiToXYZ(fault):
    "Tranforms a latitude/longitude 'Fault' to xyz coordinates"
#    if (fault.__name__ != "Fault") :   # __name__ n'existe pas. __class__ contient plus que juste le nom de la classe
#        print "Warning: calling function with wrong object"
    ret=Fault(fault.name)  #... pourl , j'oublie le nom de la faille
    for pt in fault.points :
        ret.add_point(PtLatiLongiToXYZ(pt))
    return ret

def data_to_xyz(x,y,z,dE,dN) :
    """Transforme une ligne du fichier en le deplacement tangent equivalent, proprement.
    x,y,z sont les coordonnees du point ou on le calcule ; dE, dN les deplacements nords et sud respectivement.
    Toutes les  donnees d'entree sont attendues en metres.
    """
#    from math import cos, sin, pi, sqrt
    from JDtools import Norm
# deast, dnorth sont les directions unitaires east et north respectivment.
    deastx = -y
    deasty = +x
    deastz = 0.

    nrm = Norm((deastx,deasty,deastz))
    deastx /= nrm
    deasty /= nrm
    deastz /= nrm

#    dnorth = xyz ^ deast  :
    dnorthx = -x*z
    dnorthy = -y*z
    dnorthz = x**2 + y**2

    nrm = Norm((dnorthx,dnorthy,dnorthz))
    dnorthx /= nrm
    dnorthy /= nrm
    dnorthz /= nrm

    Dispx = (deastx * dE + dnorthx * dN)
    Dispy = (deasty * dE + dnorthy * dN)
    Dispz = (deastz * dE + dnorthz * dN)

    return ( (Dispx,Dispy,Dispz) )

def data_to_xyz2(xyz,disp) :   # fixme : comment on passe differents nombres de parametres a une fonction en python ?
    "Wrapper de la fonction precedente, qui a les parametres deplies"
    if len(xyz)!=3: raise(StandardError)
    if len(disp)!=2: raise(StandardError)
    return data_to_xyz(xyz[0], xyz[1], xyz[2], disp[0], disp[1])

def dataUp_to_xyz2(xyz,disp,up) :   # fixme : comment on passe differents nombres de parametres a une fonction en python ?
    "Wrapper de la fonction precedente, qui a les parametres deplies"
    from JDtools import Norm
    if len(xyz)!=3: raise(StandardError)
    if len(disp)!=2: raise(StandardError)
    # j'ai besoin de passer par une liste temporaire parce que 'tuple' object does not support item assignment
    ret = list(data_to_xyz(xyz[0], xyz[1], xyz[2], disp[0], disp[1]))
    # et je rajoute simplement le deplacement vertical, paf !
    nrm = Norm(xyz)
    normale = map( lambda x: x/nrm , xyz)
    for i in range(len(ret)):
        ret[i] += up * normale[i]
    return tuple(ret)

def xyz_to_ENup(pt, disp):
    """Transforme un deplacement x,y,z en le deplacemet E/W N/S et vertical equivalent.
    Prend en entree les coordonnees de la station ainsi que le deplacement
    Bref, elle fait tout le contraire de data_to_xyz !
    """
# Je vais noter E,N,U le repere local
    from JDtools import Norm, CrossProduct, DotProduct
    nrm = Norm(pt)
    U = map( lambda x: x/nrm , pt)
    E = CrossProduct((0.,0.,1.),U)
    nrm = Norm(E)   # attention : U et (001) ne sont pas orthogonaux !
    E = map( lambda x: x/nrm , E)
    N = CrossProduct(U, E)
#     print "  U", U
#     print "  E", E
#     print "  N", N

    DispE = DotProduct(E,disp)
    DispN = DotProduct(N,disp)
    DispU = DotProduct(U,disp)

    return (DispE, DispN, DispU)

def _WriteVKTHeader(fic,original_name):
    "Internal use; use WriteVTK() instead"
        # VTK Header
    fic.write("# vtk DataFile Version 3.0\n")
    fic.write("Vtk translation of file " + original_name + "\n")
    fic.write("ASCII\n\nDATASET UNSTRUCTURED_GRID\n")

def _WriteVKTPoints(fic,faults):
    "Internal use; use WriteVTK() instead"
    # Points
    nbpts = 0
    for f in faults : nbpts += len(f.points)
    fic.write("POINTS " + str(nbpts) + " double\n")
    WritePoints(fic,faults)

def WritePoints(fic,faults):
    for f in faults :
        for pt in f.points :
            fic.write("%f %f %f\n"%pt)

def _WriteVKCells(fic,faults):
    "Internal use; use WriteVTK() instead"
    # Cells
    nbpts = 0
    for f in faults : nbpts += len(f.points)
    fic.write("\n")
    fic.write("CELLS %d %d\n" % (len(faults),nbpts+len(faults) ))
    counter = 0
    for f in faults :
        fic.write("%d"%len(f.points))
        for pt in f.points :
            fic.write (" %d"%counter)
            counter+=1
        fic.write("\n")

def _WriteVKCellTypes(fic,faults,cell_type):
    "Internal use; use WriteVTK() instead"
    # Cell types
    fic.write("\n")
    fic.write("CELL_TYPES %d\n"%len(faults))
    for f in faults :
        fic.write(cell_type+"\n")



def WriteVTK(fic, faults, original_name,cell_type):
    """
    Outputs (to the given output file) the list of 'Faults'
    as POLY_LINES (if cell_type="4") or POLY_VERTEX(if cell_type="2")
    """

    try:
        _WriteVKTHeader(fic,original_name)
        _WriteVKTPoints(fic,faults)
        _WriteVKCells(fic,faults)
        _WriteVKCellTypes(fic,faults,cell_type)

    except (IOError):
        print("Writing to file", fic.name, "failed")


def CheckLatiLongi(faults):
    """Checks that latitude seems ok (e.g. is below 90.).
    Developper's note: ideally this should be a method of a class 'list of faults'.
    """
    ok=True
    for f in faults:
        for pt in f.points:
            if (abs(pt[0]) > 90.):
                ok=False
                break
#     if (not ok):
#         print "Data is in longitude/latitude order. Reversing to latitude/longitude."
#         for f in faults:
#             for pt in f.points:
#                 pt = (pt[1],pt[0])
#     return faults
    if (ok):
        return faults
    else:
        # FIXME: ca devrait pas etre necessaire de faire une nouvelle liste
        print("Data is in longitude/latitude order. Reversing to latitude/longitude.")
        ret=[]
        for f in faults:
            ret.append(Fault(f.name))
            for pt in f.points:
                ret[-1].add_point((pt[1],pt[0]))
        return ret

def WriteGeof(filename,trench):
    "Writes a geof file (containing l3d2) from a Fault object"
    fic = open(filename,"w")
    fic.write("***geometry\n **node")
    fic.write("  %d 3\n"%len(trench.points) )

   # Nodes
    inode = 1
    for pt in trench.points :
        fic.write("%d "%inode)
        fic.write("%f %f %f\n"%pt)
        inode +=1


   # Elements
    inode = 0
    fic.write(" **element %d\n"%(len(trench.points)-1))
    for ielem in range(1,len(trench.points)) :
        fic.write("%d l3d2 %d %d\n"%(ielem,ielem,ielem+1))

   # Groups
    fic.write("***group\n")
    fic.write(" **nset SumatraFault\n")
    for inode in  range(1,len(trench.points)+1) :
        fic.write(" %d"%inode)
    fic.write("\n")

    fic.write(" **elset SumatraSprings\n")
    for ielem in  range(1,len(trench.points)) :
        fic.write(" %d"%ielem)
    fic.write("\n")

   # The end
    fic.write("***return\n")
    fic.close()





def GMTtoVTK(infile):
    "Converts the given gmt file to VTK format (with polylines)"
    import os

    faults = ReadGMT(infile)

    if (len(faults)>0):
        faultsXYZ=[]
        for f in faults :
            faultsXYZ.append(LatiLongiToXYZ(f))

        outfile = os.path.splitext(infile)[0] + ".vtk"
        fic = open(outfile,"w")
        WriteVTK(fic,faultsXYZ,infile,"4")
        fic.close()

    else:
        print("Not writing empty data")



class Earthquake:
    "This class is a container for earthquake data (e.g. what is available from Engdahl)"
    # should be a Dict ? ... no: too heavy
    # should be a tupple ?   neither: too order-dependent
    def __init__(self,la=0.,lo=0.,de=0.,ma=0.):
        "Sets up latitude, longitude, depth and magnitude (in that order)"
#        self.date=(yr,mon,day)
        self.lati=la
        self.longi=lo
        self.depth=de
        self.magni=ma

def ReadEngdahl(filename):
    """Reads Engdahl's file, while skipping 0-magnitude entries
    Returns a list of Earthquakes objects"""
# yr,mon,day,lat,lon,depth,ntot,max

    ret = []
    try:
        engdahl = open(filename)
        for ligne in engdahl :
            if (ligne.strip().startswith("#")) : # skip comment lines
                pass
            else :
                s = ligne.split()
                # skip 0-magnitude earthquakes
                magni = float(s[7])
                if (magni > 0.) :
                    ret.append(Earthquake( float(s[3]), float(s[4]), float(s[5]), magni ))
    except (IOError):
        print("Can't open", filename)
        print("Returning an empty list of earthquakes")
        pass
#    finally:         # mixing except and finally is not accepted before version 2.5.2
    engdahl.close()

    return ret


def EngdahltoVTK(infile):
    "Converts the given Engdahl file to VTK format (with a polyvertex)"
    import os

    engdahl_data = ReadEngdahl(infile)

    pseudofault=Fault("Engdahl Data")    # so i can reuse the WriteVTK function
    for pt in engdahl_data :
        pseudofault.add_point(PtLatiLongiToXYZ((pt.lati, pt.longi), pt.depth))
    faultsXYZ=[]
    faultsXYZ.append(pseudofault)

    outfile = os.path.splitext(infile)[0] + ".vtk"
    fic = open(outfile,'w')
    WriteVTK(fic,faultsXYZ,infile,"2")

    fic.write("\nPOINT_DATA "+str(len(engdahl_data))+"\n")
    fic.write("SCALARS SismicMag double 1\n")
    fic.write("LOOKUP_TABLE default\n")
    for d in engdahl_data :
        fic.write(str(d.magni)+"\n")
    fic.write("SCALARS profondeur double 1\n")
    fic.write("LOOKUP_TABLE default\n")
    for d in engdahl_data :
        fic.write(str(d.depth)+"\n")

    fic.close()


def determine_plane_normal(ptA, ptB, ptC):
    ### utile pour 07, define lithosphere

    vecA = np.array(ptA-ptB)
    vecB = np.array(ptA-ptC)

    normal = np.cross(vecA, vecB)

    print(normal)

    return normal



if (__name__ == "__main__"):
    # Un auto test

    #FACE NORD SLAB (tranche)
    ptA = np.array([-0.18175,-1.4068,2.49843])
    ptB = np.array([-0.18175,-1.4068,2.47881])
    ptC = np.array([-0.178024,-1.3997,2.49764])

    determine_plane_normal(ptA, ptB, ptC)

    #FACE SUD SLAB (tranche)
    ptA = np.array([-0.8237,-1.34275,2.49843])
    ptB = np.array([-0.825762,-1.33542,2.48791])
    ptC = np.array([-0.8237,-1.34275,2.47881])

    determine_plane_normal(ptA, ptB, ptC)


    #SLICE LITHO NORD
    ptA = np.array([0.226893,-1.63963,2.5])
    ptB = np.array([0.226893,-1.63963,2.47881])
    ptC = np.array([-0.18175,-1.4068,2.49843])

    determine_plane_normal(ptA, ptB, ptC)


    #SLICE LITHO SUD
    ptA = np.array([-1.0472,-1.37798,2.5])
    ptB = np.array([-1.0472,-1.37798,2.47881])
    ptC = np.array([-0.8237,-1.34275,2.47881])

    determine_plane_normal(ptA, ptB, ptC)
