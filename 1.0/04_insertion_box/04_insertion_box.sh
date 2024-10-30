#!/bin/bash -e

echo -e '\n'
echo -e '##############################'
echo -e 'Module 4 - Insertion box'
echo -e '##############################'
echo -e '\n ***START*** \n'

if [ ! -d "out" ]; then
    mkdir out
    echo -e "out dir created"
else
    rm out/*
    echo -e "out dir already exist - out dir cleaned"
fi


cp ./* ./out
cd ./out

python3 insert_slab.py
Zrun -m remplit
Zrun -m remplit -N 2

f=mesh-before-knife.geo
if [ -s $f ]; then
    echo -e '\n ***END***'
else
    echo "Error: $f is missing or empty!"
    false
fi

cd ..
