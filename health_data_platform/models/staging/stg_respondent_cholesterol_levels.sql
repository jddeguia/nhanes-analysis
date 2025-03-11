{{
    config(
      materialized='table'
    )
}}

WITH base_respondent_cholesterol_levels AS (
    SELECT *
    FROM {{ ref('base_cholesterol_labs') }}
)

SELECT * FROM base_respondent_cholesterol_levels