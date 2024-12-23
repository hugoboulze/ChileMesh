# Module 2: Slab 2D to 3D

Creation of a subduction interface. First the 2D slice of the interface is drawn. Then, it is extended along the path of the subduction trench.

At this stage, the mesh of the subducting plate has a constant dip angle.
It will be projected on the real Chilean slab in **Module 3**.

Run the following script in the current directory:

```
./02_slab_2D_to_3D.sh
```

---

## File details
---

- [`create_nodes_to_move.py`](create_nodes_to_move.py) : Define the nodes of the mesh that are allowed (or not) to move during the deformation of the slab (**Module 3**).
- [`extension.inp`](extension.inp) : Create the 3D mesh: Extension of the 2D mesh along the path of the Chilean subduction trench.
- [`refine_meshgems.inp`](refine_meshgems.inp) : Convert the 3D spherical mesh into a 3D flat frame and remesh the geometries using MeshGems.
- [`subduction_2D_chile.mast`](subduction_2D_chile.mast) : 2D geometry of the subduction zone. Open using Zmaster.
- [`check_thickness.py`](check_thickness.py) : Compute the thickness of the slab (SLAB) and of the subduction channel (CH).
- [`trench_to_geof.py`](trench_to_geof.py) : Create the `.geof` of the Chilean subduction trench from `trench_chile_34pts`.
- [`trench_chile_34pts.dat`](trench_chile_34pts.dat) : List of points picked along the Chilean subduction trench (in XYZ coordinates), e.g., using ParaView.
