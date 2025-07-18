# Module 5: Plane Cuts

Cut the mesh with:
  - Horizontal planes: -4km, -54km, -70km, -200km, -270km, -670km
  - Vertical planes: North and South of the subduction zone

Planes are inserted using Z-cracks.

<p align="center">
 <img src="../assets/step5.gif" alt="description" style="width:50%;">
</p>


Run the following script in the current directory:

```
./05_plane_cuts.sh
```

---

## File details
---

- [`create_cutting_planes.py`](create_cutting_planes.py): Build the various horizontal planes: -4km, -54km, -70km, -200km, -270km, -670km.
- [`north_south_planes.geof.tmpl`](north_south_planes.geof.tmpl): Template for the North and South vertical planes.
- [`step*.inp`](step*.inp) or [`step*.py`](step*.py): Preliminary mesh adjustments before crack insertions.
- [`zcrack2.dat`](zcrack2.dat): Crack insertion parameters, for the cut at 200, 270, and 670 km.
- [`zcrack3.dat`](zcrack3.dat): Crack insertion parameters, for the cut at 70 km.
- [`zcrack4.dat`](zcrack4.dat): Crack insertion parameters, for the cut at 54 km.
- [`zcrack5.dat`](zcrack5.dat): Crack insertion parameters, for the cut at 4 km.
- [`zcrack6.dat`](zcrack6.dat): Crack insertion parameters, for the vertical cuts between the slab's North and South extremities and corners of the bounding box.
- [`zcrack.tmpl.z7p`](zcrack.tmpl.z7p): Template batch file to run Z-cracks.
