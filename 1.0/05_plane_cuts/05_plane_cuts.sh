#!/bin/bash -e
echo -e '\n'
echo '##########################'
echo 'Module 5 - Plane cuts'
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

python3 create_cutting_planes.py

for i in $(seq 2 6); do
    echo
    echo "====> STEP $i"
    echo

    echo "     ====> Zrun -m step$i.inp"
    Zrun -m step$i.inp || { echo " ====> Aborting $0 because Zrun step$i failed." ; break; }

    [ -f step$i.py ] && python3 step$i.py

    sed -e "s/NUM/$i/" zcrack.tmpl.z7p > zcrack$i.z7p

    echo "     ====> Zrun -zp zcrack$i.z7p"
    Zrun -zp zcrack$i.z7p
done

f=mesh_knifed_NordSud_04_54_70_200_270_670.geo
if [ -s $f ]; then
    echo -e '\n ***END Knives module***'
else
    echo "Error: $f is missing or empty!"
    false
fi

cd ..
