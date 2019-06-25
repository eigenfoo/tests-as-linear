import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from utils import signed_rank, format_decimals_factory


def linear_regression_plot():
    x = np.random.normal(0, 2, 30)
    y = 0.8 * x + 0.2 * 5 * np.random.randn(30)
    df = pd.DataFrame()
    df["x"], df["y"] = x, y
    res = smf.ols("y ~ 1 + x", df).fit()
    intercept, slope = res.params

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


# pylint: disable=R0913,R0914
def pearson_spearman_plot():
    x = np.random.normal(0, 2, 30)
    y = 0.8 * x + 0.2 * 5 * np.random.randn(30)
    data_pearson = pd.DataFrame()
    data_pearson["x"], data_pearson["y"] = x, y
    res_pearson = smf.ols("y ~ 1 + x", data_pearson).fit()
    intercept_pearson, slope_pearson = res_pearson.params

    data_spearman = data_pearson.rank()
    res_spearman = smf.ols("y ~ 1 + x", data_spearman).fit()
    intercept_spearman, slope_spearman = res_spearman.params

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
        ax.scatter(dataset["x"], dataset["y"], color="k")

        # Annotate data points
        annotations = (
            "(" + dataset["x"].apply(to_str) + ", " + dataset["y"].apply(to_str) + ")"
        )
        for i, annot in enumerate(annotations):
            ax.annotate(annot, (dataset["x"][i], dataset["y"][i]), color="grey")

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


def ttest_wilcoxon_plot():
    y = np.random.normal(2, 1, 20)
    y2 = y + np.random.randn(20)

    df = pd.DataFrame()
    df["y"], df["y2"], df["y_sub_y2"] = y, y2, y-y2

    res = smf.ols(formula="y_sub_y2 ~ 1", data=df).fit()
    intercept_wilcoxon = res.params.Intercept

    fig, axarr = plt.subplots(ncols=2, figsize=[18, 8])

    axarr[0].scatter(np.zeros_like(df.y), df.y.values, color="k")
    axarr[0].scatter(np.ones_like(df.y2), df.y2.values, color="k")
    for i, j in zip(df.y, df.y2):
        axarr[0].plot([0, 1], [i, j], color="k")
    axarr[0].set_title("Pairs")

    axarr[1].scatter(np.zeros_like(df.y_sub_y2), df.y_sub_y2.values, color="k")
    annotations = df.y_sub_y2.apply(format_decimals_factory())
    for i, annot in enumerate(annotations):
        axarr[1].annotate(annot, (0, df.y_sub_y2[i]), color="grey")
    axarr[1].axhline(intercept_wilcoxon, color="b", label=r"$\beta_0$ (Intercept)")
    axarr[1].set_title("$t$-test")
    axarr[1].legend(fontsize="large")

    return fig, axarr


def pairs_wilcoxon_plot():
    y = np.random.normal(2, 1, 20)
    y2 = y + np.random.randn(20)

    df = pd.DataFrame()
    df["y"], df["y2"], df["y_sub_y2"] = y, y2, y-y2

    res = smf.ols(formula="y_sub_y2 ~ 1", data=df).fit()
    intercept_wilcoxon = res.params.Intercept

    fig, axarr = plt.subplots(ncols=2, figsize=[18, 8])

    axarr[0].scatter(np.zeros_like(df.y), df.y.values, color="k")
    axarr[0].scatter(np.ones_like(df.y2), df.y2.values, color="k")
    for i, j in zip(df.y, df.y2):
        axarr[0].plot([0, 1], [i, j], color="k")
    axarr[0].set_title("Pairs")

    axarr[1].scatter(np.zeros_like(df.y_sub_y2), df.y_sub_y2.values, color="k")
    annotations = df.y_sub_y2.apply(format_decimals_factory())
    for i, annot in enumerate(annotations):
        axarr[1].annotate(annot, (0, df.y_sub_y2[i]), color="grey")
    axarr[1].axhline(intercept_wilcoxon, color="b", label=r"$\beta_0$ (Intercept)")
    axarr[1].set_title("$t$-test")
    axarr[1].legend(fontsize="large")

    return fig, axarr


def dummy_coding_plot():
    N = 20
    data1 = np.random.multivariate_normal([0, 0], np.identity(2), N)
    data2 = np.random.multivariate_normal([4, 4], np.identity(2), N)
    df = pd.DataFrame(data=np.concatenate([data1, data2]), columns=["x", "y"])
    df["dummy"] = np.concatenate([np.zeros(N), np.ones(N)])

    res = smf.ols(formula="y ~ 1 + dummy", data=df).fit()
    beta0, beta1 = res.params

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
