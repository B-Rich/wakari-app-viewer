#!/bin/bash
SRC_DIR=$RECIPE_DIR/..
cd $SRC_DIR

$PYTHON setup.py install --single-version-externally-managed --record=record.tx

mkdir -p $PREFIX/etc/wakari/apps
cp $RECIPE_DIR/viewer.json $PREFIX/etc/wakari/apps/viewer.json
