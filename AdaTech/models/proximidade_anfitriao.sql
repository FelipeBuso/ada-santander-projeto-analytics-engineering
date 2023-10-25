{{ config(materialized='table') }} 

SELECT COUNT(*) AS tot_host, (
        SELECT COUNT(*)
        FROM raw.listings
        WHERE
            host_is_superhost = 't'
    ) AS tot_super_host,
    ROUND( (
            SELECT count(*)
            FROM raw.listings
            WHERE
                host_neighbourhood = neighbourhood_cleansed
        ):: numeric / (
            SELECT count(*)
            FROM
                raw.listings
        ):: numeric,
        2
    ) * 100 AS perc_host_proximo,
    ROUND( (
            SELECT count(*)
            FROM raw.listings
            WHERE
                host_neighbourhood = neighbourhood_cleansed
                AND host_is_superhost = 't'
        ):: numeric / (
            SELECT count(*)
            FROM raw.listings
            WHERE
                host_is_superhost = 't'
        ):: numeric,
        2
    ) * 100 AS perc_superhost_proximo
FROM raw.listings