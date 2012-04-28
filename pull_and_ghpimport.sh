#!/bin/bash

oldhash=$(git rev-parse refs/heads/gh-pages)
git pull origin master
newhash=$(git rev-parse refs/heads/gh-pages)
if [ $oldhash = $newhash ]; then
    echo "Nothing to do."
else
    echo "Update gh-pages branch and push to github."
    make github
fi

