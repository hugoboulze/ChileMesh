#!/bin/bash -e
echo -e '\n'
echo '##########################'
echo 'Module 6 - Reassign Remesh'
echo '##########################'
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

Zrun -m cut_lithospheres.inp
python3 disconnect_lithospheres.py
Zrun -m cut_asthenospheres.inp
python3 disconnect_asthenospheres.py
Zrun -m reassign_elset.inp
Zrun -m remesh.inp
Zrun -m create_boundaries_and_remove_ocean.inp
Zrun duplicate_nodes_interface.inp
Zrun -m export.inp

f=mesh-Chile_v1.0.geo
if [ -s $f ]; then
    echo -e '\n ***END***'
else
    echo "Error: $f is missing or empty!"
    false
fi

cd ..
