WITH extracted_packages AS (
  SELECT 
    id,
    REGEXP_EXTRACT_ALL(
      content,
      r'\b(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    ) AS packages
  FROM `gcp-public-data-442116.github_repos_trans.py_contents`
),
deduplicated_packages AS (
  SELECT 
    id,
    ARRAY_AGG(DISTINCT package) AS unique_packages
  FROM extracted_packages, UNNEST(packages) AS package
  GROUP BY id
)
SELECT 
  id,
  unique_packages as packages
FROM deduplicated_packages
