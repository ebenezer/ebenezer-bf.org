#!/bin/bash

BASEDIR=$(cd $(dirname $0) && pwd)
LESSC=./submodules/less.js/bin/lessc

( cd "${BASEDIR}"

    echo "> Concatenate and build less/css to theme/static/css/all.min.css"
    $LESSC --compress ./swatchmaker.less > ./theme/static/css/all.min.css

    echo "> Concatenate and build js to theme/static/js/all.min.js"
    cat ./static/js/jquery-1.7.1.js \
        ./submodules/bootstrap/js/bootstrap-dropdown.js \
        ./submodules/galleria/src/galleria.js \
        ./submodules/galleria/src/plugins/flickr/galleria.flickr.js \
        ./static/js/local.js | ./submodules/UglifyJS/bin/uglifyjs \
        > ./theme/static/js/all.min.js

    echo "> Copy bootstrap/img/ files to theme/static/img/"
    rsync -avz --cvs-exclude ./submodules/bootstrap/img/* ./theme/static/img

    echo "> Copy galleria/src/themes files to theme/static/galleria-themes/"
    rsync -avz --cvs-exclude ./submodules/galleria/src/themes/* ./theme/static/galleria-themes
)
