{{ config(materialized='table') }} 

SELECT
    host_neighbourhood,
    neighbourhood_cleansed,
    host_is_superhost,
    CASE
        WHEN host_neighbourhood = neighbourhood_cleansed THEN 1
        ELSE 0
    END AS e_proximo
FROM raw.listings