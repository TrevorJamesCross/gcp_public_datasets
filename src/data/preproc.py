"""
GCP Public Datasets: Preprocess
Author: Trevor Cross
Last Updated: 11/30/24

Pull Python package data from gcp-public-data-442116.github_repos_trans.py_packages,
unnest packages array & truncate unpopular packages (these steps are performed by the
SQL query). Then, pivot, calc package pair distances, & scale. Export preprocessed data
to CSV tracked by DVC.
"""

# TODO: add arg to select top N most popular packages

# ----------------------
# ---Import Libraries---
# ----------------------

# import standard libraries
import pandas as pd

# import GCP libraries
from google.cloud import bigquery

# import system libraries
import os

# import scipy libraries
from scipy.spatial.distance import pdist, squareform

# import sklearn libraries
from sklearn.manifold import MDS

# ----------------
# ---Initialize---
# ----------------

# initialize the BigQuery client
client = bigquery.Client()

# load SQL query
query_path = os.path.join("src", "data", "pull_preproc.sql")
with open(query_path, "r") as file:
    query = file.read()

# ---------------------------------------------
# ---Execute Job & Obtain Package Occurances---
# ---------------------------------------------

# execute the query results & load to df
df = client.query(query).to_dataframe()

# obtain number of package occurances
df_occ = df["package"].value_counts()

# ------------------------------------
# ---Pivot, Calc Distances, & Scale---
# ------------------------------------

# pivot table
df = df.pivot_table(index=["id"], columns="package", aggfunc=lambda x: 1, fill_value=0)

# collect col names
col_names = df.columns

# calc hamming distance between file packages
df = pdist(df.T, metric="hamming")
df = squareform(df)
df = pd.DataFrame(df, index=col_names, columns=col_names)

# apply multi-dimensional scaling
md_scaler = MDS(dissimilarity="precomputed")
df = pd.DataFrame(
    data=md_scaler.fit_transform(df), index=col_names, columns=["V0", "V1"]
)

# ----------------------------------------------
# ---Join w/ Package Occurances & Export Data---
# ----------------------------------------------

# join w/ package occurances
df = df.join(df_occ, validate="1:1")

# define export path
export_path = os.path.join("data", "preprocessed", "package_distances.csv")

# export to CSV
df.to_csv(export_path, index=True, header=True)
