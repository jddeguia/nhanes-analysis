{{
    config(
      materialized='table'
    )
}}

WITH mart_health_insurance_questionnaire AS (
    SELECT 
        respondent_id,
        coded_response
    FROM {{ ref('mart_health_insurance_questionnaire') }}
    WHERE question_code = 'HIQ011' --covered_with_health_insurance
),

mart_demographic AS (
    SELECT 
        respondent_id,
        gender
    FROM {{ ref('mart_demographic') }}
),

gender_covered AS (
    SELECT
        d.gender,
        SUM(CASE WHEN h.coded_response = 'Yes' THEN 1 ELSE 0 END) AS covered,
        SUM(CASE WHEN h.coded_response = 'No' THEN 1 ELSE 0 END) AS not_covered
    FROM mart_demographic d
    INNER JOIN mart_health_insurance_questionnaire h ON h.respondent_id = d.respondent_id
    GROUP BY gender
)

SELECT * FROM gender_covered