SELECT path, id
FROM `bigquery-public-data.github_repos.files`
WHERE path LIKE '%.py'
