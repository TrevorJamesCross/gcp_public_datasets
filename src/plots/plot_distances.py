"""
GCP Public Datasets: Plot Package Distances
Author: Trevor Cross
Last Updated: 12/01/24

Plot distances between packages (as calculated in preproc.py) with clustering legend (as
calculated by cluster.py). Save static image locally.
"""

# ----------------------
# ---Import Libraries---
# ----------------------

# import standard libraries
import pandas as pd

# import system libraries
import os

# import plotting libraries
import plotly.express as px
import plotly.io as pio

# ---------------
# ---Pull Data---
# ---------------

# define production data path
prod_path = os.path.join("data", "production", "clustered_packages.csv")

# read data to df
df = pd.read_csv(prod_path, index_col="package")

# convert "cluster" col to str
df["cluster"] = df["cluster"].astype(str)

# ---------------
# ---Plot Data---
# ---------------

# set plotting config
size_scaler = 10**-3

# plot scatterplot of package distances
scatterplot = px.scatter(
    data_frame=df,
    x="V0",
    y="V1",
    size=df["count"].apply(lambda x: size_scaler * x),
    color="cluster",
    color_discrete_sequence=px.colors.qualitative.Bold,
    category_orders={"cluster": sorted(df["cluster"].unique(), key=int)},
)

# -----------------
# ---Export Plot---
# -----------------

# define export path
plot_path = os.path.join("plots", "package_distances.png")

# export plot
pio.write_image(scatterplot, plot_path)
