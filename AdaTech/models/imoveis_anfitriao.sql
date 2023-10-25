{{ config(materialized='table') }} 

WITH neighbourhood AS (
        SELECT
            host_neighbourhood,
            neighbourhood_cleansed,
            CASE
                WHEN host_neighbourhood = neighbourhood_cleansed THEN 1
                ELSE 0
            END AS e_proximo
        FROM listings
    )

select * from neighbourhood 