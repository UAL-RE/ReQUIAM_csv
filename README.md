# DataRepository_research_themes

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Installation Instructions](#installation-instructions)
    - [Testing Installation](#testing-installation)
- [Execution](#execution)
    - [Workflow](#workflow)
- [Versioning](#versioning)
- [Authors](#authors)
- [License](#license)

--------------

## Overview

Constructs a mapping list between research themes ("portals") and EDS/LDAP
organization code to work with our
[Figshare patron management software](https://github.com/ualibraries/DataRepository_patrons).
This code will generate a CSV file that is used for automation.

The code imports a [Google Sheet](https://docs.google.com/spreadsheets/d/1f8tNxj96g_4NW6LWAIx8s3AxRoBbwRvFIxUXMAYyVlU/edit#gid=1301862342)
that is maintained by the Data Repository Team. The advantages of using Google Docs/Sheets are:
 1. Easy of use (no need to format CSV)
 2. Advanced spreadsheet capabilities with `VLOOKUP()`, and permitting/prohibiting cells for modification
 3. Documentation capabilities via comments and version history management
 4. Ability to grant access to University of Arizona Libraries staff for coordinated maintenance

With the above Google Sheet that is imported as a CSV file using `pandas`, it
generates a CSV file called `data/research_themes.csv`.  There are two versions
of this file:
- [stable](https://raw.githubusercontent.com/ualibraries/DataRepository_research_themes/master/DataRepository_research_themes/data/research_themes.csv): Trusted version
- [develop](https://raw.githubusercontent.com/ualibraries/DataRepository_research_themes/develop/DataRepository_research_themes/data/research_themes.csv): Under development

The [workflow](#workflow) describes how version control will be conducted with
these two different branches. In general, after a maintainer implements a
change to the Google Sheet, s/he will perform an update to the `develop`
branch. Once that has been reviewed, a pull request will be done to merge the
changes into the `master` branch.

## Getting Started

These instructions will have the code running on your local or virtual machine.


### Requirements

You will need the following to have a working copy of this software. See [installation](#installation-instructions) steps:
1. Python (3.7.5)
2. [`numpy`](https://numpy.org/doc/) ([1.18.0](https://numpy.org/doc/1.18/))
3. [`pandas`](https://pandas.pydata.org/) ([0.25.3](https://pandas.pydata.org/pandas-docs/version/0.25.3/))


### Installation Instructions

#### Python and setting up a `conda` environment

First, install a working version of Python (v3.7.5).  We recommend using the
[Anaconda](https://www.anaconda.com/distribution/) package installer.

After you have Anaconda installed, you will want to create a separate `conda` environment
and activate it:

```
$ (sudo) conda create -n rsh_themes python=3.7.5
$ conda activate rsh_themes
```

Next, clone this repository into a parent folder:

```
(rsh_themes) $ cd /path/to/parent/folder
(rsh_themes) $ git clone https://github.com/ualibraries/DataRepository_research_themes.git
```

With the activated `conda` environment, you can install with the `setup.py` script:

```
(rsh_themes) $ cd /path/to/parent/folder/DataRepository_research_themes
(rsh_themes) $ (sudo) python setup.py develop
```

This will automatically installed the required `numpy` and `pandas` packages.

You can confirm installation via `conda list`

```
(rsh_themes) $ conda list datarepository-research-themes
```

You should see that the version is `0.9.0`.


### Testing Installation

To test the installation and create a temporary CSV file that does not affect
the main CSV file, the following command will run and generate a file called
`dry_run.csv`:

```
(rsh_themes) $ python DataRepository_research_themes/script_run
```


## Execution

By default, the script does a "dry run."  To execute the script and override
the main CSV file (data/research_themes.csv), include the `execute` argument

```
(rsh_themes) $ python DataRepository_research_themes/script_run --execute
```


### Workflow
The recommended workflow to commit changes on the main CSV file is as follows:
 1. First, switch to `develop` branch: `git checkout develop`
 2. Conduct a dry run execution
 3. Compare the two CSV files: 'data/research_themes.csv' and 'data/dry_run.csv'
 4. If the changes are what you expect, conduct the full execution
 5. Update the version number in README.md, `__init__.py`, and setup.py
 6. Perform a `git add` and `git commit` for 'data/research_themes.csv' and the above files to `develop`
 7. Create a pull request [here](https://github.com/ualibraries/DataRepository_research_themes/compare/develop?expand=1)
 8. Update your local git repository with `git pull --all`

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ualibraries/DataRepository_research_themes/tags).

## Authors

* Chun Ly, Ph.D. ([@astrochun](http://www.github.com/astrochun)) - [University of Arizona Libraries](https://github.com/ualibraries), [Office of Digital Innovation and Stewardship](https://github.com/UAL-ODIS)

See also the list of
[contributors](https://github.com/ualibraries/DataRepository_research_themes/contributors) who participated in this project.


## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.
