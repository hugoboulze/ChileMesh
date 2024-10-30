#!/bin/bash -e

echo -e '\n'
echo -e '##########################'
echo -e 'Module 3 - Deform slab'
echo -e '##########################'

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
python3 deform_slab_iterative.py
Zrun round_subduction.inp
python3 check_thickness.py

f=slab_deformed_rounded_FLAT.geof
if [ -s $f ]; then
    echo -e '\n ***END***'
else
    echo "Error: $f is missing or empty!"
    false
fi

cd ..
