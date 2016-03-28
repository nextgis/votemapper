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

License
-------------
This program is licensed under GNU GPL v2 or any later version

Commercial support
----------
Need to fix a bug or add a feature to Votemapper? We provide custom development and support for this software. [Contact us](http://nextgis.ru/en/contact/) to discuss options!

[![http://nextgis.com](http://nextgis.ru/img/nextgis.png)](http://nextgis.com)
