import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

fontfamily = "Inconsolata"

sns.set_theme(style="whitegrid",
              context="paper",
              font_scale=1.25,
              rc={
                  "figure.figsize": (10.5, 4.5),
                  "figure.dpi": 250,
                  "grid.alpha": 0.1,
                  "grid.color": "#1b262c",
                  "grid.linewidth": 0.5,
                  "font.family": fontfamily
              })

_30k = ["#202f66", "#ff7048", "#7f68d0", "#f3d36e", "#d869ab", "#48ADA9", "#1b262c"]
sns.set_palette(_30k)

import warnings

warnings.filterwarnings('ignore')

from .Color import Color

DPI = 300


def plot_heatmap(dataframe, func, suptitle, vlim=(0, 100)):

    heatmap_data = []
    for i, elem1 in dataframe.iterrows():
        row = []
        for j, elem2 in dataframe.iterrows():
            row.append(func(elem1, elem2))
        heatmap_data.append(row)

    fig, ax = plt.subplots(
        nrows=2,
        ncols=2,
        figsize=(10, 10),
        dpi=DPI,
        gridspec_kw={
            'height_ratios': [10, 1],
            'width_ratios': [1, 10]
        },
    )

    vmin, vmax = vlim[0], vlim[1]

    if (vmax - vmin) // 2 >= 20:
        n_colors = (vmax - vmin) // 2
    else:
        n_colors = (vmax - vmin) * 2

    # plot heatmap
    heatmap_data = np.array(heatmap_data)
    tri_mask = np.triu(np.ones_like(heatmap_data))
    sns.heatmap(heatmap_data,
                mask=tri_mask,
                square=False,
                annot=True,
                linewidths=0.5,
                vmin=vmin,
                vmax=vmax,
                fmt='.1f',
                cmap=sns.color_palette('light:b', n_colors=n_colors),
                cbar=False,
                ax=ax[0][1])
    # hide ticks
    ax[0][1].set_xticks([], [])
    ax[0][1].set_yticks([], [])

    # vertical palette
    sns.heatmap(np.array([dataframe.index]).transpose(),
                cmap=dataframe['color'].tolist(),
                linewidths=0.5,
                cbar=False,
                ax=ax[0][0])
    ax[0][0].set_yticks(ticks=dataframe.index + 0.5, labels=dataframe['name'] + ' ' + dataframe['color'], rotation=0)
    ax[0][0].set_xticks([], [])

    # horizontal palette
    sns.heatmap([dataframe.index],
                cmap=dataframe['color'].tolist(),
                linewidths=0.5,
                cbar=False,
                ax=ax[1][1],
                square=True)
    ax[1][1].set_xticks(ticks=dataframe.index + 0.5, labels=dataframe['name'], rotation=-90)
    ax[1][1].set_yticks([], [])

    # hide unused axes
    ax[1][0].set_visible(False)

    plt.suptitle(suptitle, fontsize=24, fontweight='bold', horizontalalignment="left", y=1, x=0.1)

    plt.tight_layout(pad=1.0)
    # plt.show()

    return fig


def plot_line_vs_bg(background_colors, accent_colors, linewidth=1):
    x = np.arange(-2, 2, 0.01)

    phi_diff = 90 / len(accent_colors)

    each_axes_h = 5
    num_rows = len(background_colors)
    fig, ax = plt.subplots(num_rows,
                           1,
                           figsize=((num_rows * each_axes_h) + each_axes_h,
                                    ((num_rows * each_axes_h) + each_axes_h) // 2.5),
                           dpi=DPI)

    for i, bg_color in enumerate(background_colors):
        ax[i].set_facecolor(bg_color)
        for j, color in enumerate(accent_colors):
            sns.lineplot(x=x, y=np.sin(np.pi * x + phi_diff * j), color=color, linewidth=linewidth, ax=ax[i])
        ax[i].set_xticks([], [])
        ax[i].set_title(f"BG: {bg_color}, linewidth: {linewidth}")
        # plt.show()
    return fig