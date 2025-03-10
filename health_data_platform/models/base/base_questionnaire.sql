{{
    config(
      materialized='table'
    )
}}

WITH questionnaire_base AS (
    SELECT * 
    FROM {{ ref('questionnaire_unpivoted') }}
)

SELECT 
    SEQN as respondent_id,
    question_code,
    response,
    question_type
FROM cast_data_type