{{
    config(
      materialized='table'
    )
}}

WITH mean_cholesterol_age_group AS (
    SELECT 
        d.age_group,
        AVG(l.total_cholesterol_mgdl) AS mean_cholesterol
    FROM {{ ref('mart_demographic') }} d
    INNER JOIN {{ ref('stg_respondent_cholesterol_levels') }} l 
        ON d.respondent_id = l.respondent_id
    WHERE l.total_cholesterol_mgdl IS NOT NULL
    GROUP BY d.age_group
)

SELECT 
    a.age_group AS age_group_a,
    b.age_group AS age_group_b,
    a.mean_cholesterol AS mean_cholesterol_a,
    b.mean_cholesterol AS mean_cholesterol_b,
    CASE 
        WHEN b.mean_cholesterol = 0 THEN NULL  -- Avoid division by zero
        ELSE ((a.mean_cholesterol - b.mean_cholesterol) / b.mean_cholesterol) * 100 
    END AS percentage_difference
FROM mean_cholesterol_age_group a
INNER JOIN mean_cholesterol_age_group b 
    ON a.age_group != b.age_group
