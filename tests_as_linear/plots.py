import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from .utils import signed_rank, format_decimals_factory

plt.style.use("seaborn-whitegrid")


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


def one_way_anova_plot():
    # Construct data as a pd.DataFrame
    a = np.random.normal(0, 1, 20)
    b = np.random.normal(-2, 1, 20)
    c = np.random.normal(3, 1, 20)
    d = np.random.normal(1.5, 1, 20)

    df = pd.DataFrame()
    df["y"] = np.concatenate([a, b, c, d])
    df["group_2"] = np.concatenate(
        [np.zeros_like(b)] + [np.ones_like(b)] + 2 * [np.zeros_like(b)]
    )
    df["group_3"] = np.concatenate(
        2 * [np.zeros_like(c)] + [np.ones_like(c)] + [np.zeros_like(c)]
    )
    df["group_4"] = np.concatenate(3 * [np.zeros_like(d)] + [np.ones_like(d)])

    # ANOVA equivalent linear model
    res = smf.ols("y ~ 1 + group_2 + group_3 + group_4", df).fit()
    beta0, beta1, beta2, beta3 = res.params

    # Plot
    fig, ax = plt.subplots(figsize=[10, 8])
    ax.scatter(0 * np.ones_like(a), a, color="k")
    ax.scatter(1 * np.ones_like(b), b, color="k")
    ax.scatter(2 * np.ones_like(c), c, color="k")
    ax.scatter(3 * np.ones_like(d), d, color="k")

    # Group 1 (baseline)
    ax.axhline(beta0, color="b", label=r"$\beta_0$ (group 1 mean)")

    # Group 2
    ax.plot([0.7, 1.3], 2 * [beta0 + beta1], color="navy")
    ax.plot(
        [0, 1],
        [beta0, beta0 + beta1],
        color="r",
        label=r"$\beta_1, \beta_2, ...$ (slopes/differences to $\beta_0$)",
    )

    # Group 3
    ax.plot(
        [1.7, 2.3],
        2 * [beta0 + beta2],
        color="navy",
        label=r"$\beta_0+\beta_1, \beta_0+\beta_2 ...$ (group 2, 3 ... means)",
    )
    ax.plot([1, 2], [beta0, beta0 + beta2], color="r")

    # Group 4
    ax.plot([2.7, 3.3], 2 * [beta0 + beta3], color="navy")
    ax.plot([2, 3], [beta0, beta0 + beta3], color="r")

    ax.legend(fontsize="large")

    return fig, ax


def two_way_anova_plot(df):
    res = smf.ols("y ~ 1 + group * mood", df).fit()
    beta_0, beta_b, beta_c, beta_sad, beta_b_sad, beta_c_sad = res.params

    # Logical masks
    is_a = df["group"] == "a"
    is_b = df["group"] == "b"
    is_c = df["group"] == "c"
    is_happy = df["mood"] == "happy"
    is_sad = df["mood"] == "sad"

    # Plot
    fig, ax = plt.subplots(figsize=[10, 8])
    ax.scatter(0 * np.ones(10), df["y"][is_a & is_happy], color="r")
    ax.scatter(0 * np.ones(10), df["y"][is_a & is_sad], color="b")
    ax.scatter(1 * np.ones(10), df["y"][is_b & is_happy], color="r")
    ax.scatter(1 * np.ones(10), df["y"][is_b & is_sad], color="b")
    ax.scatter(2 * np.ones(10), df["y"][is_c & is_happy], color="r")
    ax.scatter(2 * np.ones(10), df["y"][is_c & is_sad], color="b")

    # Group a
    ax.axhline(beta_0, color="r", label="happy")
    ax.plot([-0.3, 0.3], 2 * [beta_0 + beta_sad], color="b", label="sad")

    # Group b
    ax.plot([0.7, 1.3], 2 * [beta_0 + beta_b], color="r")
    ax.plot([0.7, 1.3], 2 * [beta_0 + beta_b + beta_sad + beta_b_sad], color="b")

    # Group c
    ax.plot([1.7, 2.3], 2 * [beta_0 + beta_c], color="r")
    ax.plot([1.7, 2.3], 2 * [beta_0 + beta_c + beta_sad + beta_c_sad], color="b")

    ax.legend(fontsize="large")

    return fig, ax


def ancova_plot(df):
    # Logical masks
    is_a = df["group"] == "a"
    is_b = df["group"] == "b"
    is_c = df["group"] == "c"

    # ANCOVA equivalent linear model
    res = smf.ols("y ~ 1 + group + age", df).fit()
    beta_0, beta_b, beta_c, beta_age = res.params

    # Plot
    fig, ax = plt.subplots(figsize=[10, 8])

    ax.scatter(df[is_a]["age"], df[is_a]["y"], label="Group A", color="r")
    ax.scatter(df[is_b]["age"], df[is_b]["y"], label="Group B", color="b")
    ax.scatter(df[is_c]["age"], df[is_c]["y"], label="Group C", color="g")

    ax.plot(ax.get_xlim(), [beta_age * x + beta_0 for x in ax.get_xlim()], color="r")
    ax.plot(
        ax.get_xlim(),
        [beta_age * x + beta_0 + beta_b for x in ax.get_xlim()],
        color="b",
    )
    ax.plot(
        ax.get_xlim(),
        [beta_age * x + beta_0 + beta_c for x in ax.get_xlim()],
        color="g",
    )

    ax.set_xlabel("age", fontsize="large")
    ax.set_ylabel("y", fontsize="large")
    ax.legend(fontsize="large")

    return fig, ax
