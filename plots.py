import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from utils import signed_rank, format_decimals_factory


def linear_regression_plot():
    # Construct data as a pd.DataFrame
    x = np.random.normal(0, 2, 30)
    y = 0.8 * x + 0.2 * 5 * np.random.randn(30)
    df = pd.DataFrame()
    df["x"], df["y"] = x, y

    # Linear regression
    res = smf.ols("y ~ 1 + x", df).fit()
    intercept, slope = res.params

    # Plot
    fig, ax = plt.subplots(figsize=[10, 8])
    ax.scatter(x, y, color="k")
    ax.axhline(intercept, color="b", label=r"$\beta_0$ (Intercept)")
    ax.plot(
        ax.get_xlim(),
        [slope * x + intercept for x in ax.get_xlim()],
        color="r",
        label=r"$\beta_1$ (Slope)",
    )
    ax.legend()

    return fig, ax


# pylint: disable=R0914
def pearson_spearman_plot():
    # Construct data as pd.DataFrames
    x = np.random.normal(0, 2, 30)
    y = 0.8 * x + 0.2 * 5 * np.random.randn(30)
    data_pearson = pd.DataFrame()
    data_pearson["x"], data_pearson["y"] = x, y
    data_spearman = data_pearson.rank()

    # Pearson equivalent linear model
    res_pearson = smf.ols("y ~ 1 + x", data_pearson).fit()
    intercept_pearson, slope_pearson = res_pearson.params

    # Spearman equivalent linear model
    res_spearman = smf.ols("y ~ 1 + x", data_spearman).fit()
    intercept_spearman, slope_spearman = res_spearman.params

    # Plot
    fig, axarr = plt.subplots(ncols=2, figsize=[18, 8])

    for ax, dataset, to_str, title, a, b in zip(
        axarr,
        [data_pearson, data_spearman],
        [format_decimals_factory(), format_decimals_factory(0)],
        ["Pearson", "Spearman"],
        [slope_pearson, slope_spearman],
        [intercept_pearson, intercept_spearman],
    ):
        ax.scatter(dataset["x"], dataset["y"], color="k")

        annotations = (
            "(" + dataset["x"].apply(to_str) + ", " + dataset["y"].apply(to_str) + ")"
        )
        for i, annot in enumerate(annotations):
            ax.annotate(annot, (dataset["x"][i], dataset["y"][i]), color="grey")

        ax.axhline(a, color="b", label=r"$\beta_0$ (Intercept)")
        ax.plot(
            ax.get_xlim(),
            [a * x + b for x in ax.get_xlim()],
            color="r",
            label=r"$\beta_1$ (Slope)",
        )

        ax.set_title(title)
        ax.legend(fontsize="large")

    return fig, axarr


def ttest_wilcoxon_plot():
    # Construct data as a pd.DataFrame
    y = pd.DataFrame(data=np.random.normal(1, 1, 20), columns=["y"])

    # t-test equivalent linear model
    res = smf.ols(formula="y ~ 1", data=y).fit()
    intercept_ttest = res.params.Intercept

    # Wilcoxon equivalent linear model
    res = smf.ols(formula="y ~ 1", data=signed_rank(y)).fit()
    intercept_wilcoxon = res.params.Intercept

    # Plot
    fig, axarr = plt.subplots(ncols=2, figsize=[18, 8])

    for ax, dataset, to_str, title, b in zip(
        axarr,
        [y, signed_rank(y)],
        [format_decimals_factory(), format_decimals_factory(0)],
        ["$t$-test", "Wilcoxon"],
        [intercept_ttest, intercept_wilcoxon],
    ):
        ax.scatter(np.ones_like(dataset), dataset, color="k")

        annotations = dataset.y.apply(to_str)
        for i, annot in enumerate(annotations):
            ax.annotate(annot, (1, dataset.y[i]), color="grey")

        ax.axhline(b, color="b", label=r"$\beta_0$ (Intercept)")

        ax.set_title(title)
        ax.legend(fontsize="large")

    return fig, axarr


def pairs_wilcoxon_plot():
    # Construct data as a pd.DataFrame
    y = np.random.normal(2, 1, 20)
    y2 = y + np.random.randn(20)
    df = pd.DataFrame()
    df["y"], df["y2"], df["y_sub_y2"] = y, y2, y - y2

    # Wilcoxon equivalent linear model
    res = smf.ols(formula="y_sub_y2 ~ 1", data=df).fit()
    intercept_wilcoxon = res.params.Intercept

    # Plot
    fig, axarr = plt.subplots(ncols=2, figsize=[18, 8])

    # Left hand figure
    axarr[0].scatter(np.zeros_like(df.y), df.y.values, color="k")
    axarr[0].scatter(np.ones_like(df.y2), df.y2.values, color="k")

    for i, j in zip(df.y, df.y2):
        axarr[0].plot([0, 1], [i, j], color="k")

    axarr[0].set_title("Pairs")

    # Right hand figure
    axarr[1].scatter(np.zeros_like(df.y_sub_y2), df.y_sub_y2.values, color="k")

    annotations = df.y_sub_y2.apply(format_decimals_factory())
    for i, annot in enumerate(annotations):
        axarr[1].annotate(annot, (0, df.y_sub_y2[i]), color="grey")

    axarr[1].axhline(intercept_wilcoxon, color="b", label=r"$\beta_0$ (Intercept)")

    axarr[1].set_title("$t$-test")
    axarr[1].legend(fontsize="large")

    return fig, axarr


def dummy_coding_plot():
    # Construct data as a pd.DataFrame
    num_points = 20
    data1 = np.random.multivariate_normal([0, 0], np.identity(2), num_points)
    data2 = np.random.multivariate_normal([4, 4], np.identity(2), num_points)
    df = pd.DataFrame(data=np.concatenate([data1, data2]), columns=["x", "y"])
    df["dummy"] = np.concatenate([np.zeros(num_points), np.ones(num_points)])

    # Linear regression
    res = smf.ols(formula="y ~ 1 + dummy", data=df).fit()
    beta0, beta1 = res.params

    # Plot
    fig, ax = plt.subplots(figsize=[10, 8])
    ax.scatter(*data1.T, color="k")
    ax.scatter(*data2.T, color="k")
    ax.axhline(beta0, color="c", label=r"$\beta_0$ (group 1 mean)")
    ax.plot(
        [beta0, beta1],
        [beta0, beta1],
        color="r",
        label=r"$\beta_1$ (slope = difference)",
    )
    ax.axhline(beta1, color="b", label=r"$\beta_0 + \beta_1$ (group 2 mean)")
    ax.legend(fontsize="large")

    return fig, ax
