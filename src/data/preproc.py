"""
GCP Public Datasets: Preprocess
Author: Trevor Cross
Last Updated: 11/25/24

Pull Python package data from gcp-public-data-442116.github_repos_trans.py_packages,
unnest packages array & truncate unpopular packages. Then, pivot, calc package pair 
distances, & scale. Export preprocessed data to CSV tracked by DVC.
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
query_path = os.path.join("src", "data", "pull_packages.sql")
with open(query_path, "r") as file:
    query = file.read()

# -----------------
# ---Execute Job---
# -----------------

# execute the query results & load to df
df = client.query(query).to_dataframe()

# -----------------------
# ---Unnest & Truncate---
# -----------------------

# truncate unpopular packages (keep top 100)
print("\n> Truncating...")
package_counts = df["packages"].explode().value_counts()
top_packages = package_counts.index[:100]
print(f"\n> df.size before: {df.size}")
df = df[df["packages"].apply(lambda pkgs: any(pkg in top_packages for pkg in pkgs))]
print(f"\n> df.size after: {df.size}")

# unnest ("explode") packages col
print("\n> Exploding...")
df = df.explode("packages")

# ------------------------------------
# ---Pivot, Calc Distances, & Scale---
# ------------------------------------

# pivot table
print("\n> Pivoting...")
df = df.pivot_table(index=["id"], columns="packages", aggfunc=lambda x: 1, fill_value=0)

# collect col names
col_names = df.columns

# calc hamming distance between file packages
print("\n> Calculating Distances...")
df = pdist(df.T, metric="hamming")
df = squareform(df)
df = pd.DataFrame(df, index=col_names, columns=col_names)

# apply multi-dimensional scaling
print("\n> Scaling...")
md_scaler = MDS(dissimilarity="precomputed")
df = pd.DataFrame(
    data=md_scaler.fit_transform(df), index=col_names, columns=["V0", "V1"]
)

# -----------------
# ---Export Data---
# -----------------

# define export path
export_path = os.path.join("data", "preprocessed", "package_distances.csv")

# export to CSV
print("\n Exporting...")
df.to_csv(export_path, index=True, header=True)
