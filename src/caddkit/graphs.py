"""
This module provides utilities for analyzing and visualizing physicochemical properties 
of molecules, particularly for evaluating compliance with drug-likeness rules such as 
the "Rule of Five."

Functions:
----------
1. `calculate_mean_std(dataframe)`: 
   Computes the mean and standard deviation of specified properties in a dataset.

2. `scale_by_thresholds(stats, thresholds, scaled_threshold)`:
   Scales mean and standard deviation values for different properties based on defined thresholds.

3. `_define_radial_axes_angles(n_axes)`:
   Defines angles (in radians) for radial axes in radar charts.

4. `plot_radar(y, thresholds, scaled_threshold, properties_labels, y_max=None, output_path=None, filter_func=None)`:
   Plots a radar chart to visualize the mean and standard deviation of molecular properties 
   compared to defined thresholds.

Usage:
------
This module can be used to analyze molecular datasets, calculate descriptive statistics, 
scale properties based on thresholds, and visualize the data using radar charts. 
It is particularly useful for evaluating the compliance of molecules with drug-likeness 
criteria such as Lipinski's Rule of Five.

Dependencies:
-------------
- pandas: For data manipulation and statistical calculations.
- matplotlib: For generating radar plots.
- math: For trigonometric calculations required in radar plots.

Example:
--------
# Define thresholds and other parameters
thresholds = {"molecular_weight": 500, "n_hba": 10, "n_hbd": 5, "logp": 5}
scaled_threshold = 5
properties_labels = [
    "Molecular weight (Da) / 100",
    "# HBA / 2",
    "# HBD",
    "LogP",
]
y_max = 8

# Prepare dataset (e.g., molecules_ro5_fulfilled)
molecules_ro5_fulfilled_stats = calculate_mean_std(
    molecules_ro5_fulfilled[["molecular_weight", "n_hba", "n_hbd", "logp"]]
)

# Plot radar chart
plot_radar(
    molecules_ro5_fulfilled_stats,
    thresholds,
    scaled_threshold,
    properties_labels,
    y_max,
)
"""

import math
import matplotlib.pyplot as plt
import pandas as pd

def calculate_mean_std(dataframe):
    """
    Calculate the mean and standard deviation of a dataset.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        Properties (columns) for a set of items (rows).

    Returns
    -------
    pd.DataFrame
        Mean and standard deviation (columns) for different properties (rows).
    """
    # Generate descriptive statistics for property columns
    stats = dataframe.describe()
    # Transpose DataFrame (statistical measures = columns)
    stats = stats.T
    # Select mean and standard deviation
    stats = stats[["mean", "std"]]
    return stats

def scale_by_thresholds(stats, thresholds, scaled_threshold):
    """
    Scale values for different properties that have each an individually defined threshold.
    
    Parameters
    ----------
    stats : pd.DataFrame
        Dataframe with "mean" and "std" (columns) for each physicochemical property (rows).
    thresholds : dict of str: int
        Thresholds defined for each property.
    scaled_threshold : int or float
        Scaled thresholds across all properties.

    Returns
    -------
    pd.DataFrame
        DataFrame with scaled means and standard deviations for each physicochemical property.
    """
    for property_name in stats.index:
        if property_name not in thresholds.keys():
            raise KeyError(f"Add property '{property_name}' to scaling variable.")
    # Scale property data
    stats_scaled = stats.apply(lambda x: x / thresholds[x.name] * scaled_threshold, axis=1)
    return stats_scaled

def _define_radial_axes_angles(n_axes):
    """Define angles (radians) for radial (x-)axes depending on the number of axes."""
    x_angles = [i / float(n_axes) * 2 * math.pi for i in range(n_axes)]
    x_angles += x_angles[:1]
    return x_angles

def plot_radar(
    y,
    thresholds,
    scaled_threshold,
    properties_labels,
    y_max=None,
    output_path=None,
    filter_func=None,
):
    """
    Plot a radar chart based on the mean and standard deviation of a data set's properties.
    
    Parameters
    ----------
    y : pd.DataFrame
        Dataframe with "mean" and "std" (columns) for each physicochemical property (rows).
    thresholds : dict of str: int
        Thresholds defined for each property.
    scaled_threshold : int or float
        Scaled thresholds across all properties.
    properties_labels : list of str
        List of property names to be used as labels in the plot.
    y_max : None or int or float
        Set maximum y value. If None, let matplotlib decide.
    output_path : None or pathlib.Path
        If not None, save plot to file.
    filter_func : callable, optional
        A custom filter function to apply to the data before plotting (e.g., REOS, Lipinski).
    """
    # Apply custom filter if provided
    if filter_func:
        y = filter_func(y)

    # Define radial x-axes angles
    x = _define_radial_axes_angles(len(y))
    # Scale y-axis values with respect to a defined threshold
    y = scale_by_thresholds(y, thresholds, scaled_threshold)
    # Since our chart will be circular we append the first value of each property to the end
    y = pd.concat([y, y.head(1)])

    # Set figure and subplot axis
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    # Plot data
    ax.fill(x, [scaled_threshold] * len(x), "cornflowerblue", alpha=0.2)
    ax.plot(x, y["mean"], "b", lw=3, ls="-")
    ax.plot(x, y["mean"] + y["std"], "orange", lw=2, ls="--")
    ax.plot(x, y["mean"] - y["std"], "orange", lw=2, ls="-.")

    # Plot cosmetics
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(180)
    plt.xticks(x, [])
    if not y_max:
        y_max = int(ax.get_yticks()[-1])
    plt.ylim(0, y_max)
    plt.yticks(
        range(1, y_max),
        ["5" if i == scaled_threshold else "" for i in range(1, y_max)],
        fontsize=16,
    )

    # Draw ytick labels
    for i, (angle, label) in enumerate(zip(x[:-1], properties_labels)):
        if angle == 0:
            ha = "center"
        elif 0 < angle < math.pi:
            ha = "left"
        elif angle == math.pi:
            ha = "center"
        else:
            ha = "right"
        ax.text(
            x=angle,
            y=y_max + 1,
            s=label,
            size=16,
            horizontalalignment=ha,
            verticalalignment="center",
        )

    # Add legend relative to top-left plot
    labels = ("mean", "mean + std", "mean - std", "rule of five area")
    ax.legend(labels, loc=(1.1, 0.7), labelspacing=0.3, fontsize=16)

    # Save plot if output_path is provided
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight", transparent=True)

    plt.show()

# Example usage
# if __name__ == "__main__":
#     thresholds = {"molecular_weight": 500, "n_hba": 10, "n_hbd": 5, "logp": 5}
#     scaled_threshold = 5
#     properties_labels = [
#         "Molecular weight (Da) / 100",
#         "# HBA / 2",
#         "# HBD",
#         "LogP",
#     ]
#     y_max = 8
#     molecules = pd.DataFrame
#     molecules_ro5_fulfilled = molecules["smiles"].apply(calculate_ro5_properties)
#     # Assuming molecules_ro5_fulfilled is a predefined DataFrame
#     molecules_ro5_fulfilled_stats = calculate_mean_std(
#         molecules_ro5_fulfilled[["molecular_weight", "n_hba", "n_hbd", "logp"]]
#     )

#     plot_radar(
#         molecules_ro5_fulfilled_stats,
#         thresholds,
#         scaled_threshold,
#         properties_labels,
#         y_max,
#     )
