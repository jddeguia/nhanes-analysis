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
    WHERE question_code = 'HIQ031A' -- covered_with_private_health_insurance
      AND coded_response IN ('Yes', 'No', 'Refused', 'Unknown') -- Ensure valid responses
),

mart_demographic AS (
    SELECT 
        respondent_id,
        age_group
    FROM {{ ref('mart_demographic') }}
),

age_group_coverage AS (
    SELECT
        d.age_group,
        COUNT(*) AS total, -- Total respondents per age group
        SUM(CASE WHEN h.coded_response = 'Yes' THEN 1 ELSE 0 END) AS covered
    FROM mart_demographic d
    INNER JOIN mart_health_insurance_questionnaire h 
        ON h.respondent_id = d.respondent_id
    GROUP BY d.age_group
)

SELECT 
    age_group,
    total,
    covered,
    ROUND((covered * 100.0) / NULLIF(total, 0), 2) AS coverage_percentage
FROM age_group_coverage
ORDER BY age_group
