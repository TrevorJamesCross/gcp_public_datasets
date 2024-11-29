-- TODO: create parameter to sample P percent of IDs
SELECT path, id
FROM `bigquery-public-data.github_repos.files` TABLESAMPLE SYSTEM (10 PERCENT)
WHERE path LIKE '%.py'
