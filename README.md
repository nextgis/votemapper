# VoteMapper

Working directory:

    $ mkdir votemapper
    $ cd votemapper

Create vitrualenv:

    $ virtualenv --no-site-packages env
    $ source env/bin/activate

Install package in development mode:

    $ git clone git@github.com:nextgis/votemapper.git
    $ pip install -e votemapper

Load test data on State Duma elections of 2011 in Moscow:

    $ git clone git@github.com:nextgis/vm-2011-moscow-duma.git
    $ mkdir output
    $ votemapper vm-2011-moscow-duma/config.yaml output

As a result, bunch of static files with the map and all stuff are generated in the output directory. 

Demo: http://nextgis.github.io/votemapper-data
