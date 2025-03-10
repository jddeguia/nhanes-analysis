-- SOURCE: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/HIQ_H.htm

{{
    config(
      materialized='table'
    )
}}


{% set response_map = {
    'HIQ011': {1: 'Yes', 2: 'No', 7: 'Refused', 9: 'Refused'},
    'HIQ031A': {14: 'Yes', 77: 'Refused', 99: 'Refused'},
    'HIQ031B': {15: 'Yes'},
    'HIQ031C': {16: 'Yes'},
    'HIQ031D': {17: 'Yes'},
    'HIQ031E': {18: 'Yes'},
    'HIQ031F': {19: 'Yes'},
    'HIQ031G': {20: 'Yes'},
    'HIQ031H': {21: 'Yes'},
    'HIQ031J': {23: 'Yes'},
    'HIQ031AA': {40: 'Yes'},
    'HIQ260': {1: 'Yes', 2: 'No', 7: 'Refused', 9: 'Refused'},
    'HIQ105': {1: 'Yes', 2: 'No'},
    'HIQ270': {1: 'Yes', 2: 'No', 7: 'Refused', 9: 'Refused'},
    'HIQ210': {1: 'Yes', 2: 'No', 7: 'Refused', 9: 'Refused'}
} %}

WITH health_insurance_questionnaire AS (
    SELECT *
    FROM {{ ref('base_health_insurance_questionnaire') }}
),

add_short_definition AS (
    SELECT *,
        CASE
            WHEN question_code = 'HIQ031C' THEN 'is_covered_by_medigap'
            WHEN question_code = 'HIQ260' THEN 'has_medicare'
            WHEN question_code = 'HIQ031B' THEN 'is_covered_by_medicare'
            WHEN question_code = 'HIQ031E' THEN 'is_covered_by_schip'
            WHEN question_code = 'HIQ270' THEN 'plans_cover_prescriptions'
            WHEN question_code = 'HIQ031F' THEN 'is_covered_by_military_healthcare'
            WHEN question_code = 'HIQ031G' THEN 'is_covered_by_indian_health_service'
            WHEN question_code = 'HIQ011' THEN 'is_covered_by_health_insurance'
            WHEN question_code = 'HIQ031J' THEN 'is_covered_by_single_service_plan'
            WHEN question_code = 'HIQ210' THEN 'no_insurance_within_last_year'
            WHEN question_code = 'HIQ031A' THEN 'is_covered_by_private_insurance'
            WHEN question_code = 'HIQ105' THEN 'has_available_insurance_card'
            WHEN question_code = 'HIQ031H' THEN 'is_covered_by_state_sponsored_health_plan'
            WHEN question_code = 'HIQ031AA' THEN 'has_no_coverage_of_any_type'
            WHEN question_code = 'HIQ031D' THEN 'is_covered_by_medicaid'
            WHEN question_code = 'HIQ031I' THEN 'is_covered_by_govt_insurance'
            ELSE 'Unknown'
        END AS short_definition
    FROM health_insurance_questionnaire
),

updated_responses AS (
    SELECT *,
        CASE
            {% for key, value_map in response_map.items() %}
                {% for code, desc in value_map.items() %}
                    WHEN question_code = '{{ key }}' AND response = {{ code }} THEN '{{ desc }}'
                {% endfor %}
            {% endfor %}
            WHEN response IS NULL THEN 'Unknown'  -- Default to 'No' if response is missing
            ELSE 'No'  -- Default to 'No' if response is not mapped
        END AS coded_response
    FROM add_short_definition
)

SELECT 
    respondent_id,
    question_code,
    definition,
    short_definition,
    coded_response,
FROM updated_responses