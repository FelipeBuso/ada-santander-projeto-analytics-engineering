{{ config(materialized='table') }} 

SELECT COUNT(*) AS tot_host, (
        SELECT COUNT(*)
        FROM trusted.listings
        WHERE
            host_is_superhost
    ) AS tot_super_host,
    ROUND( (
            SELECT count(*)
            FROM
                trusted.listings
            WHERE
                host_neighbourhood = neighbourhood_cleansed
        ):: numeric / (
            SELECT count(*)
            FROM
                trusted.listings
        ):: numeric,
        2
    ) * 100 AS perc_host_proximo,
    ROUND( (
            SELECT count(*)
            FROM
                trusted.listings
            WHERE
                host_neighbourhood = neighbourhood_cleansed
                AND host_is_superhost
        ):: numeric / (
            SELECT count(*)
            FROM
                trusted.listings
            WHERE
                host_is_superhost
        ):: numeric,
        2
    ) * 100 AS perc_superhost_proximo
FROM trusted.listings