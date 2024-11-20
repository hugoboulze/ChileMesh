# Module 6: Reassign & Remesh

Create the final geometries (e.g. asthenosphere, lithosphere) and remesh their elements according to the distance to the fault plane.

Run the following script in the current directory:

```
./06_reassign_remesh.sh
```

---

## File details
---

- [`create_boundaries_and_remove_ocean.inp`](#) : Create group of nodes for boundary conditions, remove the ocean geometry, and transform the mesh in 3D spherical coordinates.
- [`create_mmg_metric.py`](#) : Reassign the different parts of the mesh to create the final geometries of the mesh (e.g., asthenosphere, lithosphere).
- [`cut_asthenospheres.inp`](#) : Cut the asthenosphere according to vertical planes to separate the oceanic and continental parts.
- [`cut_lithospheres.inp`](#) : Cut the lithosphere according to vertical planes to separate the oceanic and continental parts.
- [`disconnect_asthenospheres.py`](#) : Disconnect oceanic and continental asthenospheres.
- [`disconnect_lithospheres.py`](#) : Disconnect oceanic and continental lithospheres.
- [`duplicate_nodes_interface.inp`](#) : Insert a crack along the fault plane and duplicate nodes along the fault plane.
- [`export.inp`](#) : Export the mesh in different formats.
- [`reassign_elset.inp`](#) : Reassign the different parts of the mesh to create the final geometries of the mesh (e.g., asthenosphere, lithosphere).
- [`remesh.inp`](#) : Final mesh refinement using MMG, with element sizes depending on the distance to the fault plane.
