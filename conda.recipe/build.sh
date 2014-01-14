#!/bin/bash
SRC_DIR=$RECIPE_DIR/..
cd $SRC_DIR

cd ..
$PYTHON setup.py install

mkdir -p $PREFIX/etc/wakari/apps
cp $RECIPE_DIR/viewer.json $PREFIX/etc/wakari/apps/viewer.json
