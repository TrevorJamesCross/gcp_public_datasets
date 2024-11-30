"""
GCP Public Datasets: Plot Package Distances
Author: Trevor Cross
Last Updated: 11/30/24

Plot distances between packages (as calculated in preproc.py) with clustering legend (as
calculated by cluster.py). Save figure locally.
"""

# ----------------------
# ---Import Libraries---
# ----------------------

# import standard libraries
import pandas as pd

# import system libraries
import os

# import plotting libraries
import seaborn as sns

# ---------------
# ---Pull Data---
# ---------------

# define production data path
prod_path = os.path.join("data", "production", "clustered_packages.csv")

# read data to df
df = pd.read_csv(prod_path, index_col="package")

# ---------------
# ---Plot Data---
# ---------------

# set plotting config
sns.set_theme(style="darkgrid")
size_scaler = 10**-3

# plot scatterplot of package distances
scatterplot = sns.scatterplot(
    data=df,
    x=df["V0"],
    y=df["V1"],
    size=df["count"].apply(lambda x: size_scaler * x),
    hue=df["cluster"],
    palette=sns.color_palette("husl", len(df["cluster"].unique())),
    legend=False,
)

# -----------------
# ---Export Plot---
# -----------------

# define export path
plot_path = os.path.join("plots", "package_distances.png")

# export plot
sns_fig = scatterplot.get_figure()
sns_fig.savefig(plot_path)
