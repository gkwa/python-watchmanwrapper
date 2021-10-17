========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-watchmanwrapper/badge/?style=flat
    :target: https://python-watchmanwrapper.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/ionelmc/python-watchmanwrapper.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/ionelmc/python-watchmanwrapper

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-watchmanwrapper?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-watchmanwrapper

.. |requires| image:: https://requires.io/github/ionelmc/python-watchmanwrapper/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-watchmanwrapper/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/ionelmc/python-watchmanwrapper/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-watchmanwrapper

.. |version| image:: https://img.shields.io/pypi/v/watchmanwrapper.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/watchmanwrapper

.. |wheel| image:: https://img.shields.io/pypi/wheel/watchmanwrapper.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/watchmanwrapper

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/watchmanwrapper.svg
    :alt: Supported versions
    :target: https://pypi.org/project/watchmanwrapper

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/watchmanwrapper.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/watchmanwrapper

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-watchmanwrapper/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-watchmanwrapper/compare/v0.0.0...master



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install watchmanwrapper

You can also install the in-development version with::

    pip install https://github.com/ionelmc/python-watchmanwrapper/archive/master.zip


Documentation
=============


https://python-watchmanwrapper.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
