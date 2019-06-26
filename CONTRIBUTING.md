# Contributing Guide

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
├── Makefile
├── README.md
├── index.html             # Generated HTML.
├── plots.py               # Functions for large plots in main notebook.
├── requirements.txt       # Python package dependencies.
├── scripts                # Shell scripts for development, testing and deployment.
│   └── ...
├── tests-as-linear.ipynb  # Main notebook.
└── utils.py               # Utility functions used in main notebook.
```

## Development guide

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
