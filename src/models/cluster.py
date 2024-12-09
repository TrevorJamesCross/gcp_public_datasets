"""
GCP Public Datasets: Cluster Package Distances
Author: Trevor Cross
Last Updated: 12/03/24

Run clustering algorithm on package distances & export new data locally.
"""

# TODO: add args for clustering method parameters

# ----------------------
# ---Import Libraries---
# ----------------------

# import standard libraries
import pandas as pd

# import system libraries
import os

# import clustering libraries
from sklearn.cluster import AffinityPropagation

# ---------------
# ---Pull Data---
# ---------------

# define preprocessed data path
preproc_path = os.path.join("data", "preprocessed", "package_distances.csv")

# read data to df
df = pd.read_csv(preproc_path, index_col="package")

# ----------------------
# ---Cluster Packages---
# ----------------------

# init clustering object
cluster_obj = AffinityPropagation()

# fit clustering algo & append to df
df["cluster"] = cluster_obj.fit_predict(df[["V0", "V1"]])

# -----------------
# ---Export Data---
# -----------------

# define export path
prod_path = os.path.join("data", "production", "clustered_packages.csv")

# export data
df.to_csv(prod_path, header=True, index=True)
