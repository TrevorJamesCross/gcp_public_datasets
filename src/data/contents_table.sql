SELECT content, id
FROM `bigquery-public-data.github_repos.contents`
WHERE id IN (SELECT id FROM `gcp-public-data-442116.github_repos_trans.py_files`)
AND content IS NOT NULL
AND content != ''
AND id IS NOT NULL
AND id != ''
