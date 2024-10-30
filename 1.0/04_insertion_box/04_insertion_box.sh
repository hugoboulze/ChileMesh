#!/bin/bash -e

cat <<EOF

##############################
Module 4 - Insertion box
##############################
***START***

EOF

rm -rf out
rsync -a . out/ --exclude=out --exclude=$(basename $0)
cd out/

# for constants.py:
export PYTHONPATH=$PWD/../..:${PYTHONPATH}

python3 insert_slab.py
Zrun -m fill_volume.inp
Zrun -m fill_volume.inp -N 2

f=mesh-before-knife.geo
if [ -s $f ]; then
    echo -e '\n ***END***'
else
    echo "Error: $f is missing or empty!"
    false
fi
