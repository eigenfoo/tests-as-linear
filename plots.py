import numpy as np
import matplotlib.pyplot as plt
from utils import signed_rank, format_decimals_factory


def linear_regression_plot(data, intercept, slope):
    fig, ax = plt.subplots(figsize=[10, 8])
    ax.scatter(data["y"], data["x"], color="k")
    ax.axhline(intercept, color="b", label=r"$\beta_0$ (Intercept)")
    ax.plot(
        ax.get_xlim(),
        [slope * x + intercept for x in ax.get_xlim()],
        color="r",
        label=r"$\beta_1$ (Slope)",
    )
    ax.legend()

    return fig, ax


# pylint: disable=R0913,R0914
def pearson_spearman_plot(
    data_pearson,
    data_spearman,
    slope_pearson,
    slope_spearman,
    intercept_pearson,
    intercept_spearman,
):
    fig, axarr = plt.subplots(ncols=2, figsize=[18, 8])

    for ax, dataset, to_str, title, a, b in zip(
        axarr,
        [data_pearson, data_spearman],
        [format_decimals_factory(), format_decimals_factory(0)],
        ["Pearson", "Spearman"],
        [slope_pearson, slope_spearman],
        [intercept_pearson, intercept_spearman],
    ):
        # Plot
        ax.scatter(dataset["y"], dataset["x"], color="k")

        # Annotate data points
        annotations = (
            "(" + dataset["x"].apply(to_str) + ", " + dataset["x"].apply(to_str) + ")"
        )
        for i, annot in enumerate(annotations):
            ax.annotate(annot, (dataset["y"][i], dataset["x"][i]), color="grey")

        # Plot lines
        ax.axhline(a, color="b", label=r"$\beta_0$ (Intercept)")
        ax.plot(
            ax.get_xlim(),
            [a * x + b for x in ax.get_xlim()],
            color="r",
            label=r"$\beta_1$ (Slope)",
        )

        # Decorate
        ax.set_title(title)
        ax.legend(fontsize="large")

    return fig, axarr


def ttest_wilcoxon_plot(data, intercept_ttest, intercept_wilcoxon):
    fig, axarr = plt.subplots(ncols=2, figsize=[18, 8])

    for ax, dataset, to_str, title, b in zip(
        axarr,
        [data.y, signed_rank(data.y)],
        [format_decimals_factory(), format_decimals_factory(0)],
        ["$t$-test", "Wilcoxon"],
        [intercept_ttest, intercept_wilcoxon],
    ):
        # Scatter plot
        ax.scatter(np.ones_like(dataset), dataset, color="k")

        # Annotate data points
        annotations = dataset.apply(to_str)
        for i, annot in enumerate(annotations):
            ax.annotate(annot, (1, dataset[i]), color="grey")

        # Plot lines
        ax.axhline(b, color="b", label=r"$\beta_0$ (Intercept)")

        # Decorate
        ax.set_title(title)
        ax.legend(fontsize="large")

    return fig, axarr
