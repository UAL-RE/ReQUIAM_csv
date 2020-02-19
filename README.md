# DataRepository_research_themes
Construct list of research themes and organization mapping to work with figshare patron management

## Getting Started

These instructions will have the code running on your local or virtual machine.


### Prerequisites

The following will be needed
1. python (3.7.5)
2. [`numpy`](https://numpy.org/doc/) ([1.18.0](https://numpy.org/doc/1.18/))
3. [`pandas`](https://pandas.pydata.org/) ([0.25.3](https://pandas.pydata.org/pandas-docs/version/0.25.3/))

First, you would need to have a working version of Python (v3.7.5).  We recommend using the
[Anaconda](https://www.anaconda.com/distribution/) package installer.

After you have Anaconda installed, you will want to create a separate `conda` environment
and activate it:

```
$ (sudo) conda create -n rsh_themes python=3.7.5
$ conda activate rsh_themes
```

### Installation

To install, you will need to clone this repository into what ever parent folder you wish to use:

```
$ cd /path/to/parent/folder
$ git clone https://github.com/ualibraries/DataRepository_research_themes.git
```

With the activated `conda` environment, you can install with the `setup.py` script:

```
$ cd /path/to/parent/folder/DataRepository_research_themes
$ python setup.py develop
```

This will automatically installed the required `numpy` and `pandas` packages.

You can confirm installation via `conda list`

```
$ conda list datarepository-research-themes
```

You should see that the version is `0.5.0`.


### Running the tests

Will fill in later.


## Execution

To execute the script
```
$ python DataRepository_research_themes/script_run
```


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ualibraries/DataRepository_research_themes/tags).

## Authors

* [Chun Ly](http://www.github.com/astrochun) - [University of Arizona Libraries](https://github.com/ualibraries), [Office of Digital Innovation and Stewardship](https://github.com/UAL-ODIS)

See also the list of
[contributors](https://github.com/ualibraries/DataRepository_research_themes/contributors) who participated in this project.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
