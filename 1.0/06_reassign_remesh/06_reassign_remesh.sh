#!/bin/bash -e

cat <<EOF

##############################
Module 6 - Reassign Remesh
##############################
***START***

EOF

rm -rf out
rsync -a . out/ --exclude=out --exclude=$(basename $0)
cd out/

Zrun -m cut_lithospheres.inp
python3 disconnect_lithospheres.py
Zrun -m cut_asthenospheres.inp
python3 disconnect_asthenospheres.py
Zrun -m reassign_elset.inp
python3 create_mmg_metric.py
Zrun -m remesh.inp
Zrun -m create_boundaries_and_remove_ocean.inp
Zrun -m duplicate_nodes_interface.inp
Zrun -m export.inp

f=mesh-Chile_v1.0.geo
if [ -s $f ]; then
    echo -e '\n ***END***'
else
    echo "Error: $f is missing or empty!"
    false
fi
