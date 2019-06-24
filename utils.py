""" Utility functions. """

import re
import json
import numpy as np
import pandas as pd


def signed_rank(x, axis=-1):
    return np.sign(x) * np.argsort(x, axis=axis)


def format_decimals_factory(num_decimals=1):
    return lambda x: "{1:.{0}f}".format(num_decimals, x)


def tabulate_results(test_values, ols_results, names, x=True):
    # There may be only one OLS result. If so, wrap it up as a single list.
    if not isinstance(ols_results, list):
        ols_results = [ols_results]

    # Assert shapes
    assert len(test_values) == 5
    assert len(names) == len(ols_results) + 1

    # Construct and return table
    table = pd.DataFrame(index=names)
    coeff = "x" if x else "Intercept"
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


def generate_toc(notebook="tests-as-linear.ipynb"):
    """
    Generates a table of contents in Markdown.

    Assumes that headers begin with `#` symbols (e.g. there is no leading
    whitespace). Considers all symbols after the consecutive `#` symbols (there
    may be more than one) to be the header.

    Parameters
    ----------
    notebook : str
        Path to notebook for which to generate a table of contents.

    Returns
    -------
    toc : str
        Table of contents as a Markdown string.
    """
    with open(notebook, "r") as f:
        cells = json.load(f)["cells"]

    items = ["# Table of contents"]
    for cell in cells:
        if cell["cell_type"] == "markdown":
            for line in cell["source"]:
                match = re.search(r"^#+ ", line)
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
