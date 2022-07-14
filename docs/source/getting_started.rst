Getting Started
===============

Requirements
------------

You will need the following to have a working copy of this software. See
`installation <#installation-instructions>`__ steps:

1. Python (>=3.8)
2. `numpy <https://numpy.org/doc/>`__ (`1.23.0 <https://numpy.org/doc/1.23/>`__)
3. `pandas <https://pandas.pydata.org/>`__ (`1.4.3 <https://pandas.pydata.org/docs/whatsnew/v1.4.3.html>`__)

Installation Instructions
-------------------------

Python and setting up a ``conda`` environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You have already followed the same installation instructions 
from `ReQUIAM <https://requiam.readthedocs.io/en/latest/getting_started.html>`

Next, clone this repository into a parent folder:

::

   (admin1) $ cd /path/to/parent/folder
   (admin1) $ git clone https://github.com/UAL-RE/ReQUIAM_csv.git

With the activated ``conda`` environment, you can install with the
``setup.py`` script:

::

   (admin1) $ cd /path/to/parent/folder/ReQUIAM_csv
   (admin1) $ (sudo) python setup.py develop

This will automatically installed the required ``numpy`` and ``pandas``
packages. The versions shall be the same as these of redata-commons and ReQUIAM.

You can confirm installation via ``conda list``

::

   (rsh_themes) $ conda list requiam_csv

You should see that the version is ``0.13.0``.

Configuration Settings
----------------------

Configuration settings are specified through the
`default.ini <https://github.com/UAL-RE/ReQUIAM_csv/blob/master/requiam_csv/default.ini>`__ file. These settings
include the Google Sheet information and CSV file names (do **not**
change as this will break ReQUIAM).

Testing Installation
--------------------

To test the installation and create a temporary CSV file that does not
affect the main CSV file, the following command will run and generate a
file called ``dry_run.csv``:

::

   (rsh_themes) $ python requiam_csv/script_run
