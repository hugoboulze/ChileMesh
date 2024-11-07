#!/bin/bash -e

cat <<EOF

##########################
Module 3 - Deform slab
##########################

EOF

rm -rf out
rsync -a . out/ --exclude=out --exclude=$(basename $0)
cd out/

# for tools.py:
export PYTHONPATH=$PWD/../..:${PYTHONPATH}

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
