{{ config(materialized='table') }} 

WITH neighbourhood_counts AS (
        SELECT
            host_neighbourhood,
            COUNT(*) AS neighbourhood_count,
            AVG(
                CAST(
                    REPLACE(
                            REPLACE
(price, '$', ''),
                                ',',
                                ''
                        ) AS numeric
                )
            ) AS avg_price
        FROM listings
        GROUP BY
            host_neighbourhood
    )

select * from neighbourhood_counts 