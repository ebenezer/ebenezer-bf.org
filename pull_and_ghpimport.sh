#!/bin/bash

oldhash=$(git rev-parse HEAD)
git pull origin master
newhash=$(git rev-parse HEAD)
if [ "$oldhash" == "$newhash" ]; then
    echo "Nothing to do."
else
    echo "Update gh-pages branch and push to github."
    make github
fi

