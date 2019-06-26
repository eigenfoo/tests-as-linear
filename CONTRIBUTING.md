# Contributing Guide

[![GitHub Issues](https://img.shields.io/github/issues/eigenfoo/tests-as-linear.svg)](https://github.com/eigenfoo/tests-as-linear/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/eigenfoo/tests-as-linear.svg)](https://github.com/eigenfoo/tests-as-linear/pulls)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](https://github.com/eigenfoo/tests-as-linear/blob/master/CODE_OF_CONDUCT.md)

Contributions are always welcome! Check out the GitHub issue trackers for both
[this Python port](https://github.com/eigenfoo/tests-as-linear/issues) and/or
the [original R post](https://github.com/lindeloev/tests-as-linear/issues) for
some ideas on how to contribute.

- Raise issues if you have ideas.
- Submit pull requests if you want to help improve these resources.
- Star this repo if you want to follow updates.
- Fork this repo if you want to make your own spin!

## Project structure

```bash
.
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── Makefile
├── README.md
├── index.html             # Published HTML.
├── plots.py               # Functions for large plots in main notebook.
├── requirements-dev.txt   # Dependencies for development.
├── requirements.txt       # Dependencies.
├── scripts                # Shell scripts for development, testing and deployment.
│   └── ...
├── tests-as-linear.ipynb  # Main notebook.
└── utils.py               # Utility functions used in main notebook.
```

## Development instructions

```bash
git clone git@github.com:<USERNAME>/tests-as-linear.git
cd tests-as-linear/
make venv
source venv/bin/actviate
# Do your work...
make publish
make check
deactivate
```

Please make sure that `make publish` and `make check` successfully complete
before committing and pushing: these commands generate publishable HTML files,
lint the Python modules and run various test scripts.
