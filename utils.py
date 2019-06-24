""" Utility functions. """

import re
import json


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
