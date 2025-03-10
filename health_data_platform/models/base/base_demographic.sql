{{
    config(
      materialized='table'
    )
}}

{% set rename_dict = {
    "AIALANGA": "language",
    "DMDBORN4": "respondent_birth_country",
    "DMDCITZN": "respondent_us_citizen",
    "DMDEDUC2": "respondent_education_level",
    "DMDEDUC3": "respondent_education_level_detailed",
    "DMDFMSIZ": "family_size",
    "DMDHHSIZ": "household_size",
    "DMDHHSZA": "children_5_or_younger",
    "DMDHHSZB": "children_6_to_17",
    "DMDHHSZE": "adults_60_or_older",
    "DMDHRAGE": "household_head_age",
    "DMDHRBR4": "household_head_birth_country",
    "DMDHREDU": "household_head_education_level",
    "DMDHRGND": "household_head_gender",
    "DMDHRMAR": "household_head_marital_status",
    "DMDHSEDU": "household_spouse_education_level",
    "DMDMARTL": "marital_status",
    "DMDYRSUS": "years_lived_in_us",
    "DMQADFC": "military_foreign_service",
    "DMQMILIZ": "military_service",
    "FIAINTRP": "fia_interpreter_used",
    "FIALANG": "fia_language_spoken",
    "FIAPROXY": "fia_proxy_respondent",
    "INDFMIN2": "family_income_range",
    "INDFMPIR": "income_poverty_ratio",
    "INDHHIN2": "household_income_range",
    "MIAINTRP": "mia_interpreter_used",
    "MIALANG": "mia_language_spoken",
    "MIAPROXY": "mia_proxy_respondent",
    "RIAGENDR": "gender",
    "RIDAGEMN": "age_in_months_screening",
    "RIDAGEYR": "age_in_years_screening",
    "RIDEXAGM": "age_in_months_exam",
    "RIDEXMON": "exam_six_month_period",
    "RIDEXPRG": "pregnancy_status",
    "RIDRETH1": "race_ethnicity",
    "RIDRETH3": "race_ethnicity_detailed",
    "RIDSTATR": "participant_status",
    "SDDSRVYR": "survey_data_release_cycle",
    "SDMVPSU": "variance_unit_psu",
    "SDMVSTRA": "variance_unit_stratum",
    "SEQN": "respondent_id",
    "SIAINTRP": "sia_interpreter_used",
    "SIALANG": "sia_language_spoken",
    "SIAPROXY": "sia_proxy_respondent",
    "WTINT2YR": "interview_weight_2yr",
    "WTMEC2YR": "mec_exam_weight_2yr"
} %}

with rename_column AS (
    SELECT
        {% for old_col, new_col in rename_dict.items() %}
            {{ old_col }} AS {{ new_col }}{% if not loop.last %}, {% endif %}
        {% endfor %}
    FROM {{ ref('demographic') }}
)

SELECT * FROM rename_column