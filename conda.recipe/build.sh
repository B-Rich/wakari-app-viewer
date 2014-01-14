#!/bin/bash
SRC_DIR=$RECIPE_DIR/..
cd $SRC_DIR

mkdir -p $PREFIX/share/wakari/html
cp -r static/* $PREFIX/share/wakari/html/viewer

cd ..
$PYTHON setup.py install

mkdir -p $PREFIX/etc/wakari/apps
cp $RECIPE_DIR/viewer.json $PREFIX/etc/wakari/apps/viewer.json
