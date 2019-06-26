# _Common statistical tests are linear models_: Python port

[![Build Status](https://travis-ci.com/eigenfoo/tests-as-linear.svg?branch=master)](https://travis-ci.com/eigenfoo/tests-as-linear)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/eigenfoo/tests-as-linear/master?filepath=tests-as-linear.ipynb)

A Python port of Jonas Kristoffer Lindeløv's post [_Common statistical tests are
linear models (or: how to teach
stats)_](https://lindeloev.github.io/tests-as-linear/), which originally had
accompanying code in R.

## Notes on Python port

The original post used R's built-in functions to verify that the linear models
were indeed equivalent to the statistical tests (by showing that the p-values,
t-values, and other such statistics, were the same in either case). In this
Python port, we instead verify that `scipy.stats` functions and `smf.ols` output
agree.

The original R post had [four
appendices](https://github.com/lindeloev/tests-as-linear/tree/master/simulations),
each of which demonstrated (through numerical simulation) that a common
statistical test was well-approximated by a linear model. These simulations have
not been ported to Python (yet!). This is [an outstanding
issue](https://github.com/eigenfoo/tests-as-linear/issues/14). In the meantime,
please refer to the [original appendices
upstream](https://github.com/lindeloev/tests-as-linear/tree/master/simulations)
for the simulations.

## Contributing

Please refer to [the contributing
guide](https://github.com/eigenfoo/tests-as-linear/blob/master/CONTRIBUTING.md)
for project structure information and development instructions.
