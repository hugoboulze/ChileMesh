#!/bin/bash -e

cat <<EOF
################################
Module 2 - Slab 2D to 3D
################################
EOF

rm -rf out
rsync -a . out/ --exclude=out
cd out/

echo -e '\n ***START*** \n'
python3 trench_to_geof.py trench_chile_34pts.dat
Zrun -B subduction_2D_chile.mast
Zrun -m extension.inp
python3 create_nodes_to_move.py
Zrun -m refine_meshgems.inp

f=slab_refined_FLAT.geof
if [ -s $f ]; then
    echo "out/$f succesfully created"
    echo -e '\n ***END***'
else
    echo "Error: $f is missing or empty!"
    false
fi
