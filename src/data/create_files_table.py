"""
GCP Public Datasets: Create Files Table
Author: Trevor Cross
Last Updated: 11/21/24

Programmatically create a table in BigQuery that contains all file paths
ending in ".py" from GCP public dataset (bigquery-public-data.github_repos).
"""

# ----------------------
# ---Import Libraries---
# ----------------------

# import GCP libraries
from google.cloud import bigquery

# import system libraries
import os

# ------------------------------------
# ---Initialize & Define Job Config---
# ------------------------------------

# initialize the BigQuery client
client = bigquery.Client()

# load SQL query
query_path = os.path.join("src", "data", "files_table.sql")
with open(query_path, "r") as file:
    query = file.read()

# define destination table id
dest_id = "gcp-public-data-442116.github_repos_trans.py_files"

# define a job configuration
job_config = bigquery.QueryJobConfig(
    destination=dest_id,
    write_disposition="WRITE_TRUNCATE",
)

# -----------------
# ---Execute Job---
# -----------------

# execute the query
query_job = client.query(query, job_config=job_config)

# wait for the job to complete
query_job.result()
