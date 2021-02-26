Overview
========

Constructs a mapping list between research themes (“portals”) and
EDS/LDAP organization code to work with our `Figshare patron management
software (ReQUIAM) <https://github.com/ualibraries/ReQUIAM>`__. This
code will generate a CSV file that is used for automation. The code
imports a `Google
Sheet <https://docs.google.com/spreadsheets/d/1f8tNxj96g_4NW6LWAIx8s3AxRoBbwRvFIxUXMAYyVlU/edit#gid=1301862342>`__
that is maintained by the Data Repository Team. The advantages of using
Google Sheets are: 1. Easy of use (no need to format CSV) 2. Advanced
spreadsheet capabilities with ``MATCH()``, and permitting/prohibiting
cells for modification 3. Documentation capabilities via comments and
version history management 4. Ability to grant access to University of
Arizona Libraries staff for coordinated maintenance

With the above Google Sheet that is imported as a CSV file using
``pandas``, it generates a CSV file called
```data/research_themes.csv`` <requiam_csv/data/research_themes.csv>`__.
There are two versions of this file: - Trusted version, ``master``:
`[raw] <https://raw.githubusercontent.com/ualibraries/ReQUIAM_csv/master/requiam_csv/data/research_themes.csv>`__
`[rendered] <https://github.com/ualibraries/ReQUIAM_csv/blob/master/requiam_csv/data/research_themes.csv>`__
- Under developement, ``develop``:
`[raw] <https://raw.githubusercontent.com/ualibraries/ReQUIAM_csv/develop/requiam_csv/data/research_themes.csv>`__
`[rendered] <https://github.com/ualibraries/ReQUIAM_csv/blob/develop/requiam_csv/data/research_themes.csv>`__

The `workflow <#workflow>`__ describes how version control will be
conducted with these two different branches. In general, after a
maintainer implements a change to the Google Sheet, s/he will perform an
update to the ``develop`` branch. Once that has been reviewed, a pull
request will be done to merge the changes into the ``master`` branch.
