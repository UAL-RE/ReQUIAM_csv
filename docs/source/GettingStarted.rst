Getting Started
===============

These instructions will have the code running on your local or virtual
machine.

Requirements
------------

You will need the following to have a working copy of this software. See
`installation <#installation-instructions>`__ steps: 1. Python (3.7.5)
2. ```numpy`` <https://numpy.org/doc/>`__
(`1.18.0 <https://numpy.org/doc/1.18/>`__) 3.
```pandas`` <https://pandas.pydata.org/>`__
(`0.25.3 <https://pandas.pydata.org/pandas-docs/version/0.25.3/>`__)

Installation Instructions
-------------------------

Python and setting up a ``conda`` environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, install a working version of Python (v3.7.5). We recommend using
the `Anaconda <https://www.anaconda.com/distribution/>`__ package
installer.

After you have Anaconda installed, you will want to create a separate
``conda`` environment and activate it:

::

   $ (sudo) conda create -n rsh_themes python=3.7.5
   $ conda activate rsh_themes

Next, clone this repository into a parent folder:

::

   (rsh_themes) $ cd /path/to/parent/folder
   (rsh_themes) $ git clone https://github.com/ualibraries/ReQUIAM_csv.git

With the activated ``conda`` environment, you can install with the
``setup.py`` script:

::

   (rsh_themes) $ cd /path/to/parent/folder/ReQUIAM_csv
   (rsh_themes) $ (sudo) python setup.py develop

This will automatically installed the required ``numpy`` and ``pandas``
packages.

You can confirm installation via ``conda list``

::

   (rsh_themes) $ conda list requiam_csv

You should see that the version is ``0.11.0``.

Configuration Settings
----------------------

Configuration settings are specified through the
```default.ini`` <requiam_csv/default.ini>`__ file. These settings
include the Google Sheet information and CSV file names (do **not**
change as this will break ReQUIAM).

Testing Installation
--------------------

To test the installation and create a temporary CSV file that does not
affect the main CSV file, the following command will run and generate a
file called ``dry_run.csv``:

\``\` (rsh_themes) $ python requiam_csv/script_run
