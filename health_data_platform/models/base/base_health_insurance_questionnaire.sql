{{
    config(
      materialized='table'
    )
}}

WITH questionnaire_base AS (
    SELECT * 
    FROM {{ ref('questionnaire_Health_Insurance') }}
),

questionnaire_definition AS (
    SELECT 
        variable_name AS question_code,
        variable_description AS definition
    FROM {{ ref('base_questionnaire_code_definition') }}
),

summary AS (
    SELECT
        qb.SEQN as respondent_id,
        qb.question_code,
        qb.response,
        qb.question_type,
        qd.definition
    FROM questionnaire_base qb
    LEFT JOIN questionnaire_definition qd ON qd.question_code = qb.question_code
)

SELECT * FROM summary