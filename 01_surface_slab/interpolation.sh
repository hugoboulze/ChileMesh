#!/bin/bash -e
# interpolation of the slab in the Patagona region, using GMT
DIR=./
gmt greenspline -R-90/-60/-60/0 $DIR/train.dat -G$DIR/interp.nc -I15m -Z2 -Sl -V
gmt grdtrack $DIR/evaluate.dat -G$DIR/interp.nc -N > $DIR/evaluate_slab.dat
