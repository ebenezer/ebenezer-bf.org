ebenezer-bf.org
===============

Ce dépôt contient les sources utilisées pour générer le site web statique du
Centre Eben-Ezer.

Nous utilisons le moteur Pelican_ pour effectuer la génération des fichiers
html.

.. _`Pelican`: http://pelican.notmyidea.org

Pour installer ce projet, il suffit de lancer les commandes suivantes::

    $ python bootstrap.py
    $ ./buildout/bin/buildout

Ensuite vous pouvez générer le site web dans le répertoire `_output`::

    $ source ./buildout/bin/activate
    (ebenezer-bf.org) $ make html

Pour lancer une regénération du site automatique à chaque modification, vous
pouvez utiliser la commande suivante::

    (ebenezer-bf.org) $ pelican -o _output/ -s pelican.conf.py -r -d
