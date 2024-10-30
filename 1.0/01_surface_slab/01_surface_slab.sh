#!/bin/bash -e

cat <<EOF
##########################
Module 1 - Surface slab
##########################
EOF

# Recreate a fresh and clean out directory:
rm -rf out
rsync -a . out/ --exclude=out --exclude=$(basename $0)
cd out/

echo -e '\n ***START*** \n'
python3 create_surface_slab.py
echo -e '\n ***END***'

f=slabSurf_0.1deg_SPHE.csv
if [ -s $f ]; then
    echo "out/$f succesfully created"
    echo -e '\n ***END***'
else
    echo "Error: out/$f is missing or empty!"
fi
