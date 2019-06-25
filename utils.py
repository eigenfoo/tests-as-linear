""" Utility functions. """

import re
import json
import numpy as np
import pandas as pd


def signed_rank(df):
    return np.sign(df) * df.abs().rank()


def format_decimals_factory(num_decimals=1):
    return lambda x: "{1:.{0}f}".format(num_decimals, x)


def tabulate_results(test_values, ols_results, names, coeff="x"):
    """
    Tabulates results of statistical tests and equivalent linear regressions to
    demonstrate that the two methods are in fact equivalent.

    Parameters
    ----------
    test_values : list
        List of values from the scipy statistical test to display.
    ols_results : statsmodels.RegressionResults or list thereof
        Result object(s) of equivalent linear regression to display.
    names : list
        List of strings to display.
    coeff : str
        Name of coefficient whose test statistics should be displayed. Defaults
        to "x".

    Returns
    -------
    table : pd.DataFrame
    """
    # There may be only one OLS result. If so, wrap it up as a single list.
    if not isinstance(ols_results, list):
        ols_results = [ols_results]

    # Assert shapes
    assert len(test_values) == 5
    assert len(names) == len(ols_results) + 1

    # Construct and return table
    table = pd.DataFrame(index=names)
    table["value"] = [test_values[0]] + [res.params[coeff] for res in ols_results]
    table["p-values"] = [test_values[1]] + [res.pvalues[coeff] for res in ols_results]
    table["t-values"] = [test_values[2]] + [res.tvalues[coeff] for res in ols_results]
    table["0.025 CI"] = [test_values[3]] + [
        res.conf_int().loc[coeff, 0] for res in ols_results
    ]
    table["0.975 CI"] = [test_values[4]] + [
        res.conf_int().loc[coeff, 1] for res in ols_results
    ]

    return table


def generate_toc(notebook="tests-as-linear.ipynb", max_header_levels=2):
    """
    Generates a table of contents in Markdown.

    Assumes that headers begin with `#` symbols (e.g. there is no leading
    whitespace). Considers all symbols after the consecutive `#` symbols (there
    may be more than one) to be the header.

    Parameters
    ----------
    notebook : str
        Path to notebook for which to generate a table of contents.
    max_header_levels : int
        Maximum number of header levels to show in table of contents (i.e. the
        depth of headers to display).

    Returns
    -------
    toc : str
        Table of contents as a Markdown string.
    """
    with open(notebook, "r") as f:
        cells = json.load(f)["cells"]

    items = ["# Contents"]
    for cell in cells:
        if cell["cell_type"] == "markdown":
            for line in cell["source"]:
                match = re.search(r"^[#]{{1,{0}}} ".format(max_header_levels), line)
                if match:
                    level = len(line) - len(line.lstrip("#"))
                    link = line.strip(" #\n").replace(" ", "-")
                    items.append(
                        2 * (level - 1) * " "
                        + "- ["
                        + line.strip(" #\n")
                        + "](#"
                        + link
                        + ")"
                    )

    toc = "\n".join(items)
    return toc
