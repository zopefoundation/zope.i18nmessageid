Hacking on :mod:`zope.i18nmessageid`
====================================


Getting the Code
################

The main repository for :mod:`zope.i18nmessageid` is in the Zope Foundation
Github repository:

  https://github.com/zopefoundation/zope.i18nmessageid

You can get a read-only checkout from there:

.. code-block:: sh

   $ git clone https://github.com/zopefoundation/zope.i18nmessageid.git

or fork it and get a writeable checkout of your fork:

.. code-block:: sh

   $ git clone git@github.com/jrandom/zope.i18nmessageid.git


Working in a Python virtual environment
#######################################

Installing
----------

You can use Python's standard ``venv`` package to create lightweight Python
development environments, where you can run the tests using nothing more
than the ``python`` binary in a virtualenv.  First, create a scratch
environment:

.. code-block:: sh

   $ python3.12 -m venv /tmp/hack-zope.i18nmessageid

Next, install this package in "development mod" in the newly-created
environment:

.. code-block:: sh

   $ /tmp/hack-zope.i8nmessageid/bin/pip install -e .

Running the tests
-----------------

Once installed,  you can run the tests using the standard library's
``unittest`` module:

.. code-block:: sh

   $ /tmp/hack-zope.i8nmessageid/bin/python -m unittest discover -s src
   .........................................
   ----------------------------------------------------------------------
   Ran 41 tests in 0.002s

   OK

You can install a more comprehensive set of tools using the ``testing``
extra:

.. code-block:: sh

   $ /tmp/hack-zope.i8nmessageid/bin/pip install -e ".[testing]"


That command installs the tools needed to run
the tests:  in particular, the ``zope.testrunner`` (see
:external+testrunner:std:doc:`getting-started`) and
:external+coverage:std:doc:`index` tools.

To run the tests via ``zope.testrunner``:

.. code-block:: sh

   $ /tmp/hack-zope.i8nmessageid/bin/zope-testrunner --test-path=src
   Running zope.testrunner.layer.UnitTests tests:
     Set up zope.testrunner.layer.UnitTests in 0.000 seconds.
     Ran 41 tests with 0 failures, 0 errors and 0 skipped in 0.003 seconds.
   Tearing down left over layers:
     Tear down zope.testrunner.layer.UnitTests in 0.000 seconds.

Running the tests under :mod:`coverage` lets you see how well the tests
cover the code:

.. code-block:: sh

   $ /tmp/hack-zope.i8nmessageid/bin/coverage run -m zope.testrunner \
      --test-path=src
   ...
   $ coverage report -i -m --fail-under=100
   Name                                 Stmts   Miss Branch BrPart    Cover   Missing
   ----------------------------------------------------------------------------------
   src/zope/i18nmessageid/__init__.py       4      0      0      0  100.00%
   src/zope/i18nmessageid/message.py       52      0     18      0  100.00%
   src/zope/i18nmessageid/tests.py        189      0     38      0  100.00%
   ----------------------------------------------------------------------------------
   TOTAL                                  245      0     56      0  100.00%


Building the documentation
--------------------------

:mod:`zope.i18nmessageid` uses the nifty :mod:`Sphinx` documentation system
for building its docs.  Using the same virtualenv you set up to run the
tests, you can build the docs:

The ``docs`` command alias downloads and installs Sphinx and its dependencies:

.. code-block:: sh

   $ /tmp/hack-zope.i8nmessageid/bin/pip install ".[docs]"
   ...
   $ /tmp/hack-zope.i8nmessageid/bin/sphinx-build -b html -d docs/_build/doctrees docs docs/_build/html
   ...
   build succeeded.

   The HTML pages are in docs/_build/html.

You can also test the code snippets in the documentation:

.. code-block:: sh

   $ /tmp/hack-zope.i8nmessageid/bin/sphinx-build -b doctest -d docs/_build/doctrees docs docs/_build/doctest
   ...
   running tests...

   Document: narr
   --------------
   1 items passed all tests:
     35 tests in default
   35 tests in 1 items.
   35 passed and 0 failed.
   Test passed.

   Doctest summary
   ===============
      35 tests
       0 failures in tests
       0 failures in setup code
       0 failures in cleanup code
   build succeeded.

   Testing of doctests in the sources finished, look at the results in docs/_build/doctest/output.txt.


Using :mod:`tox`
################


Running Tests on Multiple Python Versions
-----------------------------------------

`tox <http://tox.testrun.org/latest/>`_ is a Python-based test automation
tool designed to run tests against multiple Python versions.  It creates
a virtual environment for each configured version, installs the current
package and configured dependencies into each environment, and then runs the
configured commands.
   
:mod:`zope.i18nmessageid` configures the following :mod:`tox` environments via
its ``tox.ini`` file:

- The ``lint`` environment runs various "code quality" tests on the source,
  and fails on any errors they find.

- The ``py38``, ``py39``, ``py310``, ``py311``, ``py312``, ``py313``, and
  ``pypy3`` environments each build an environment from the corresponding
  Python version, install :mod:`zope.i18nmessageid` and testing dependencies,
  and runs the tests.  It then installs ``Sphinx`` and runs the doctest
  snippets.

- The ``coverage`` environment builds a virtual environment,
  installs :mod:`zope.i18nmessageid` and dependencies, installs
  :mod:`coverage`, and runs the tests with statement and branch
  coverage.

- The ``docs`` environment builds a virtual environment, installs
  :mod:`zope.i18nmessageid` and dependencies, installs ``Sphinx`` and
  dependencies, and then builds the docs and exercises the doctest snippets.

This example requires that you have a working ``python3.12`` on your path,
as well as installing ``tox``:

.. code-block:: sh

   $ tox -e py312
   py312: install_deps> python -I -m pip install 'setuptools<69' Sphinx
   ...
   py312: commands[0]> zope-testrunner --test-path=src -vc
   Running tests at level 1
   Running zope.testrunner.layer.UnitTests tests:
     Set up zope.testrunner.layer.UnitTests in 0.000 seconds.
     Running:
   .........................................
     Ran 41 tests with 0 failures, 0 errors, 0 skipped in 0.003 seconds.
   Tearing down left over layers:
     Tear down zope.testrunner.layer.UnitTests in 0.000 seconds.
   py312: commands[1]> sphinx-build -b doctest -d /home/tseaver/projects/Zope/Z3/zope.i18nmessageid/.tox/py312/.cache/doctrees docs /home/tseaver/projects/Zope/Z3/zope.i18nmessageid/.tox/py312/.cache/doctest
   Running Sphinx v7.3.7
   ...
   running tests...

   Document: narr
   --------------
   1 items passed all tests:
     35 tests in default
   35 tests in 1 items.
   35 passed and 0 failed.
   Test passed.

   Doctest summary
   ===============
      35 tests
       0 failures in tests
       0 failures in setup code
       0 failures in cleanup code
   build succeeded.

   Testing of doctests in the sources finished, look at the results in .tox/py312/.cache/doctest/output.txt.
     py312: OK (16.29=setup[15.11]+cmd[0.26,0.92] seconds)
     congratulations :) (16.56 seconds)

Running ``tox`` with no arguments runs all the configured environments,
including building the docs and testing their snippets:

.. code-block:: sh

   $ tox
   lint: commands[0]> isort --check-only --diff /home/tseaver/projects/Zope/Z3/zope.i18nmessageid/src /home/tseaver/projects/Zope/Z3/zope.i18nmessageid/setup.py
   lint: commands[1]> flake8 src setup.py
     lint: OK (0.50=setup[0.02]+cmd[0.19,0.28] seconds)
     congratulations :) (0.73 seconds)
   ...
   __________________________________ summary ____________________________________
   lint: commands succeeded
   py37: commands succeeded
   ...
   pypy3: commands succeeded
   docs: commands succeeded
   coverage: commands succeeded
   congratulations :)


Contributing to :mod:`zope.i18nmessageid`
#########################################

Submitting a Bug Report
-----------------------

:mod:`zope.i18nmessageid` tracks its bugs on Github:

  https://github.com/zopefoundation/zope.i18nmessageid/issues

Please submit bug reports and feature requests there.

Sharing Your Changes
--------------------

.. note::

   Please ensure that all tests are passing before you submit your code.
   If possible, your submission should include new tests for new features
   or bug fixes, although it is possible that you may have tested your
   new code by updating existing tests.

If have made a change you would like to share, the best route is to fork
the Githb repository, check out your fork, make your changes on a branch
in your fork, and push it.  You can then submit a pull request from your
branch:

  https://github.com/zopefoundation/zope.i18nmessageid/pulls
