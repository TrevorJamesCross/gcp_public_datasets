-- unnest the packages col
WITH unnested_packages AS (
    SELECT
        id,
        package
    FROM
        `gcp-public-data-442116.github_repos_trans.py_packages`,
        UNNEST(packages) AS package
),

-- count occurrences of each package & keep top 100
package_counts AS (
    SELECT
        package,
        COUNT(*) AS package_count
    FROM
        unnested_packages
    GROUP BY
        package
    ORDER BY
        package_count DESC
    LIMIT 100
)

-- join back to retain associated IDs
SELECT
    u.id,
    u.package
FROM
    unnested_packages u
JOIN
    package_counts p
ON
    u.package = p.package
