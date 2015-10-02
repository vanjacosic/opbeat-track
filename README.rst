opbeat-track
============

Small dependency-free CLI tool to track releases to `Opbeat.com <https://opbeat.com>`_

The idea was to create a small script that doesn't rely on third party modules to work, so that it could be used easily on "any" system (with Python installed).

Disclaimer: I'm still new to Python, so there might be many things that can be improved. Feel free to point them out, PRs are very welcome.

Installation
------------

Install using:

    $ python setup.py install

Verify by running:

    $ opbeat-track --version

To run the package without installing use:

    $ python -m opbeat_track --version
    
Alternatively, you can also:
    
    $ chmod u+x opbeat-track-runner.py
    $ ./opbeat-track-runner.py --version


Usage
-----

    $ opbeat-track [-o ORG_ID] [-a APP_ID] [-s SECRET_TOKEN] [-b BRANCH]
    
Example:

    $ opbeat-track -a sd25403b -o 223s3438094c012bb32u55437a -s 523e0222ww8a8sf2af7e3392f224d1026s3 -b 'v2.0'

Use the help command to get an overview:

    $ opbeat-track --help


To do:
------
- Get an actual Pythonista to review it
- Write tests
- Upload to PyPi
- Implement option to load tokens from a file

Notes
-----
The project structure is borrowed from this post: https://gehrcke.de/2014/02/distributing-a-python-command-line-application/