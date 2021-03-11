Execution
=========

By default, the script does a “dry run.” To execute the script and
override the main CSV file (data/research_themes.csv), include the
``execute`` argument

::

   (rsh_themes) $ python requiam_csv/script_run --execute

.. _workflow:

Workflow
--------

The recommended workflow to commit changes on the main CSV file is as
follows:

1. First, switch to ``develop`` branch: ``git checkout develop``
2. Conduct a dry run execution
3. Compare the two CSV files: ‘data/research_themes.csv’ and ‘data/dry_run.csv’
4. If the changes are what you expect, conduct the full execution
5. Update the version number in README.md, ``__init__.py``, and setup.py
6. Perform a ``git add`` and ``git commit`` for ‘data/research_themes.csv’ and the above files to ``develop``
7. Create a pull request `here <https://github.com/UAL-ODIS/ReQUIAM_csv/compare/develop?expand=1>`__
8. Update your local git repository with ``git pull --all``
