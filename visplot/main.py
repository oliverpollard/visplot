import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
from cmcrameri import cm
import numpy as np
from itertools import combinations
from scipy.stats import gaussian_kde

plt.style.use("seaborn-v0_8-whitegrid")

views = {
    "global": {
        "plot_crs": ccrs.PlateCarree(),
        "extent": [-180, 180, -90, 90],
    },
    "eurasia": {
        "plot_crs": ccrs.LambertAzimuthalEqualArea(central_latitude=90),
        "extent": [-1053702.958, 3417796.998000001, -4560734.802, 1115265.2419999992],
    },
}


def text(ax, text, x=0.5, y=0.95, fontsize=14):
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontweight="bold",
        fontsize=fontsize,
        color="white",
        bbox=dict(boxstyle="round", facecolor="black"),
        zorder=20,
    )


def plot_map(figsize=None, grid=None, plot_crs=None, extent=None, text=None, gl=True):
    if plot_crs is None:
        plot_crs = ccrs.LambertAzimuthalEqualArea(central_latitude=90)
    if extent is None:
        extent = [-1053702.958, 3417796.998000001, -4560734.802, 1115265.2419999992]

    if grid is None:
        grid = [1, 1]
    if figsize is None:
        figsize = [15, 8]
    fig = plt.figure(figsize=figsize)
    axes = np.empty((grid[0] * grid[1]), dtype=object)
    for idx in range(grid[0] * grid[1]):
        ax = fig.add_subplot(grid[0], grid[1], idx + 1, projection=plot_crs)
        ax.add_feature(
            cartopy.feature.LAND,
            zorder=1,
            facecolor=(0, 0, 0, 0.1),
            edgecolor=(0, 0, 0, 0.5),
        )
        if gl is True:
            gridlines = ax.gridlines(draw_labels=True, linestyle="--")
            gridlines.right_labels = False
            gridlines.top_labels = False
        ax.set_extent(extent, crs=plot_crs)
        if text:
            ax.text(
                0.5,
                0.95,
                text,
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontweight="bold",
                fontsize=14,
                color="white",
                bbox=dict(boxstyle="round", facecolor="black"),
                zorder=20,
            )
        axes[idx] = ax
    axes = np.squeeze(np.reshape(axes, (grid[0], grid[1])))
    if grid[0] == grid[1] == 1:
        axes = ax
    return fig, axes


def param_plot(
    param_names,
    param_values,
    data=None,
    vmin=None,
    vmax=None,
    mirror=False,
    plot_density=False,
    plot_kwargs=None,
    ranges=None,
):
    num_params = len(param_names)
    fig, axes = plt.subplots(num_params, num_params, figsize=[15, 15], dpi=300)

    param_values = (param_values - param_values.min(axis=0)) / (
        param_values.max(axis=0) - param_values.min(axis=0)
    )

    combos = list(combinations(np.arange(num_params), 2))
    for pa_index, pb_index in combos:
        ax = axes[pa_index, pb_index]
        ax.grid(False)

        param_x = param_values[:, pb_index]
        param_y = param_values[:, pa_index]
        """
        param_x_norm = (param_x - param_x.min(axis=0)) / (
            param_x.max(axis=0) - param_x.min(axis=0)
        )
        param_y_norm = (param_y - param_y.min(axis=0)) / (
            param_y.max(axis=0) - param_y.min(axis=0)
        )
        """
        if data is not None:
            z = data
            if vmin is None:
                vmin = data.min()
            if vmax is None:
                vmin = data.max()
        elif plot_density is True:
            try:
                xy = np.vstack([param_x, param_y])
                z = gaussian_kde(xy)(xy)
            except:
                z = "C0"
            vmin = None
            vmax = None
        else:
            z = "#005f73"
            vmin = None
            vmax = None

        if plot_kwargs is None:
            plot_kwargs = {}
        if "cmap" not in plot_kwargs:
            plot_kwargs["cmap"] = "BuPu"
        if "s" not in plot_kwargs:
            plot_kwargs["s"] = 6

        img = ax.scatter(param_x, param_y, c=z, **plot_kwargs)
        """
        img1 = ax.imshow(
            t_mask_sum_norm, 
            vmin=0, 
            vmax=1,
            cmap="GnBu", 
            origin="lower",
            extent=[0,1,0,1]
        )
        """
        if ((pa_index == 0) and (pb_index % 2 == 1)) and (
            (pb_index == 6) and (pa_index % 2 == 1)
        ):
            ax.xaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
            ax.xaxis.set_ticks_position("top")
            ax.yaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
            ax.yaxis.set_ticks_position("right")
        elif (pa_index == 0) and (pb_index % 2 == 1):
            ax.xaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
            ax.axes.yaxis.set_ticklabels([])
            ax.xaxis.set_ticks_position("top")
        elif (pb_index == num_params - 1) and (pa_index % 2 == 1):
            ax.yaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
            ax.axes.xaxis.set_ticklabels([])
            ax.yaxis.set_ticks_position("right")
        else:
            ax.axes.xaxis.set_ticklabels([])
            ax.axes.yaxis.set_ticklabels([])

        ax = axes[pb_index, pa_index]
        if mirror is True:
            ax.grid(False)
            ax.scatter(param_values[pb_index], param_values[pa_index])
            if ((pa_index == 0) and (pb_index % 2 == 0)) and (
                (pb_index == 6) and (pa_index % 2 == 0)
            ):
                ax.yaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
                ax.yaxis.set_ticks_position("left")
                ax.xaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
                ax.xaxis.set_ticks_position("bottom")
            elif (pa_index == 0) and (pb_index % 2 == 0):
                ax.yaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
                ax.axes.xaxis.set_ticklabels([])
                ax.yaxis.set_ticks_position("left")
            elif (pb_index == num_params - 1) and (pa_index % 2 == 0):
                ax.xaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
                ax.axes.yaxis.set_ticklabels([])
                ax.xaxis.set_ticks_position("bottom")
            else:
                ax.axes.xaxis.set_ticklabels([])
                ax.axes.yaxis.set_ticklabels([])
        else:
            ax.axis("off")

    for index in range(num_params):
        ax = axes[index, index]
        ax.axis("off")
        ax.text(
            0.5,
            0.5,
            param_names[index],
            horizontalalignment="center",
            verticalalignment="center",
        )
    return fig, ax, img
