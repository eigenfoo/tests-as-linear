import re
import json
import string


def generate_toc(notebook="tests-as-linear.ipynb"):
    """ Generate markdown table of contents """
    with open(notebook, "r") as f:
        cells = json.load(f)["cells"]

    toc = ["# Table of contents\n"]
    for cell in cells:
        if cell["cell_type"] == "markdown":
            for line in cell["source"]:
                match = re.search("^#+ \w+", line)
                if match:
                    level = len(line) - len(line.lstrip("#"))
                    link = line.strip(" #\n").replace(" ", "-")
                    toc.append(
                        2 * (level - 1) * " "
                        + "- ["
                        + line.strip(" #\n")
                        + "](#"
                        + link
                        + ")\n"
                    )

    out = ""
    for item in toc:
        out += item

    return out
