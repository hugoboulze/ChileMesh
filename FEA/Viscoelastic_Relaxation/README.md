# How to compute viscoelastic relaxation following an earthquake?

using:
- Zset/Zebulon
- Chile_Mesh_v1.0

## 1. Finite-element computation
In a terminal, type:
```
Zrun reference_model.inp
```

##### Output:
- `reference_model.(integ, ctnod, msg, node, rst, ut)`

## 2. Post-processing
Relocating displacements at specific locations rather than nodes.

In a terminal, type:

```
Zrun -pp reference_model.inp
```

##### Output:
- ```reference_model_grid.vtk```
- ```reference_model.(msgp, post, utp)```

## 3. Generate time-series

In a terminal, type:
```
python3 pp.py
```
##### Output:
- ```reference_model_grid.dat```
- ```./tS_grid```: containing all predicted time-series of displacement for each point of the grid
