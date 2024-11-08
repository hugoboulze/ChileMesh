#!/bin/bash -e
cat <<EOF

##############################
Module 5 - Plane cuts
##############################
***START***

EOF

rm -rf out
rsync -a . out/ --exclude=out --exclude=$(basename $0)
cd out/

# for constants.py:
export PYTHONPATH=$PWD/../..:${PYTHONPATH}

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

f=mesh_knifed_north_south_04_54_70_200_270_670.geo
if [ -s $f ]; then
    echo -e '\n ***END Knives module***'
else
    echo "Error: $f is missing or empty!"
    false
fi
