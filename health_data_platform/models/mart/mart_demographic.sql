{{
    config(
      materialized='table'
    )
}}

WITH stg_demograhic_base AS (
    SELECT *
    FROM {{ ref('stg_demographic') }}
)

SELECT * FROM stg_demograhic_base