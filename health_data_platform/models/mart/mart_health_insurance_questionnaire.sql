{{
    config(
      materialized='table'
    )
}}

WITH stg_health_insurance_questionnaire AS (
    SELECT *
    FROM {{ ref('stg_health_insurance_questionnaire') }}
)

SELECT * FROM stg_health_insurance_questionnaire