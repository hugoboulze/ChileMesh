# Module 1: Surface Slab

Creation of point on the surface of the slab based on Slab2.0 ([Hayes et al. 2018](https://www.science.org/doi/10.1126/science.aat4723)).
The surface will be used to project the slab in the **Module 3**.

Run the following script in the current directory:

```
./01_surface_slab.sh
```

---

## File details
---

- [`interpolation.sh`](interpolation.sh): Interpolation (using GMT) of the southern part of the slab (Patagonia region).
- [`create_surface_slab.py`](create_surface_slab.py): Build the surface of the slab used in **Module 3** as a .csv file.
- [`sam_slab2_dep_02.23.18.xyz`](sam_slab2_dep_02.23.18.xyz): Slab2.0 model (Hayes et al. 2018) from [ScienceBase Catalog](https://www.sciencebase.gov/catalog/item/5aa41473e4b0b1c392eaaf2d).
- [`trench_Chile.gmt`](trench_Chile.gmt): Path - (lon, lat) in degrees - of the Chilean subduction trench (from GMT).
