pl-benchmark-matrixmulti
================================

.. image:: https://badge.fury.io/py/benchmark_matrixmulti.svg
    :target: https://badge.fury.io/py/benchmark_matrixmulti

.. image:: https://travis-ci.org/FNNDSC/benchmark_matrixmulti.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/benchmark_matrixmulti

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-benchmark_matrixmulti

.. contents:: Table of Contents


Abstract
--------

An app to ...


Synopsis
--------

.. code::

    python benchmark_matrixmulti.py                                           \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 

Description
-----------

``benchmark_matrixmulti.py`` is a ChRIS-based application that...

Agruments
---------

.. code::

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install benchmark_matrixmulti

and run with

.. code:: bash

    benchmark_matrixmulti.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    benchmark_matrixmulti.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-benchmark_matrixmulti benchmark_matrixmulti.py                        \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-benchmark_matrixmulti benchmark_matrixmulti.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------





