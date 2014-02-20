#!/bin/bash
SRC_DIR=$RECIPE_DIR/..
cd $SRC_DIR

$PYTHON setup.py install

mkdir -p $PREFIX/etc/wakari/apps
cp $RECIPE_DIR/viewer.json $PREFIX/etc/wakari/apps/viewer.json

POST_LINK=$PREFIX/bin/.${PKG_NAME}-post-link.sh
cp $RECIPE_DIR/post-link.sh $POST_LINK
chmod +x $POST_LINK
