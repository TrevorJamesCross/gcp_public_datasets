"""
GCP Public Datasets: Get Raw Table Metadata
Author: Trevor Cross
Last Updated: 11/22/24

Programmatically get metadata from raw BigQuery tables
bigquery-public-data.github_repos.{files, .contents} and update params.yaml. This script
is ran at the start of the pipeline to conditionally run create_{files, contents}_tables
.py scripts.
"""

# ----------------------
# ---Import Libraries---
# ----------------------

# import GCP libraries
from google.cloud import bigquery

# import system libraries
import yaml

# ----------------
# ---Initialize---
# ----------------

# init BigQuery client
client = bigquery.Client()

# define public table IDs in dict
dict_ids = {
    key: "bigquery-public-data.github_repos." + key for key in ["files", "contents"]
}

# ------------------------------------------
# ---Obtain Metadata & Update params.yaml---
# ------------------------------------------

# read params.yaml
params = yaml.safe_load(open("params.yaml", "r"))

# iterate dict_ids key-value pairs
for key, id_ in dict_ids.items():

    # get table
    table = client.get_table(id_)

    # get metadata from table
    last_modified_time = table.modified

    # update last_modified value
    params[f"create_{key}_table"]["last_modified"] = last_modified_time.isoformat()

# dump new params.yaml
yaml.safe_dump(params, open("params.yaml", "w"))
