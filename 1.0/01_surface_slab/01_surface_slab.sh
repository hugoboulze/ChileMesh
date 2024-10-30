#!/bin/bash -e

echo -e '\n'
echo '##########################'
echo 'Module 1 - Surface slab'
echo '##########################'

if [ ! -d "out" ]; then
    mkdir out
    echo -e "out dir created"
else
    rm -f out/*
    echo -e "out dir already exist - out dir cleaned"
fi

cp ./* ./out
cd ./out

echo -e '\n ***START*** \n'
python3 create_surface_slab.py
echo -e '\n ***END***'

f=slabSurf_0.1deg_SPHE.csv
if [ -s $f ]; then
    
    echo $f succesfully created
    echo -e '\n ***END***'
 
else
    echo "Error: $f is missing or empty!"
    false
fi

cd ..
