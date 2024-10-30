#!/bin/bash -e

echo -e '\n'
echo -e '################################'
echo -e 'Module 2 - Slab 2D to 3D'
echo -e '################################'

if [ ! -d "out" ]; then
    mkdir out
    echo -e "out dir created"
else
    rm out/*
    echo -e "out dir already exist - out dir cleaned"
fi

cp ./* ./out
cd ./out

Zclean -a

echo -e '\n ***START*** \n'
python3 trench_to_geof.py trench_chile_34pts.dat
Zrun -B subduction_2D_chile.mast
mv subduction_2D_chile.geof ./out/
Zrun -m extension.inp
python3 create_nodes_to_move.py
Zrun -m refine_meshgems.inp

f=slab_refined_FLAT.geof
if [ -s $f ]; then
    
    echo $f succesfully created
    echo -e '\n ***END***'
 
else
    echo "Error: $f is missing or empty!"
    false
fi

cd ..
