-- the source is https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/DEMO_H.htm?fbclid=IwY2xjawI72pNleHRuA2FlbQIxMAABHSRQauvkCEyaWqI4VnD_Yhpi6wf4l0f8HAzSmUdg3bWLDecCNZ82dUnoIA_aem_zzHPY4TUCk9D7jPAyrQScQ#RIDRETH1

{{
    config(
      materialized='table'
    )
}}

WITH base_demographic AS (
    SELECT *
    FROM {{ ref('base_demographic') }}
),

impute_values AS (
    SELECT
        respondent_id,
        CASE
            WHEN language = 1 THEN 'English'
            WHEN language = 2 THEN 'Spanish'
            WHEN language = 3 THEN 'Asian Languages'
            ELSE 'Unknown'
        END AS language,
        CASE 
            WHEN respondent_birth_country = 1 THEN 'USA'
            WHEN respondent_birth_country = 2 THEN 'Outside USA'
            WHEN respondent_birth_country IN (77, 99) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS respondent_birth_country,
        CASE
            WHEN respondent_us_citizen = 1 THEN 'Citizen'
            WHEN respondent_us_citizen = 2 THEN 'Not a Citizen'
            WHEN respondent_us_citizen IN (7, 9) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS respondent_us_citizen,
        CASE
            WHEN respondent_education_level = 1 THEN '< 9th Grade'
            WHEN respondent_education_level = 2 THEN '9 - 11th Grade'
            WHEN respondent_education_level = 3 THEN 'High School Graduate'
            WHEN respondent_education_level = 4 THEN 'AA Degree'
            WHEN respondent_education_level = 5 THEN 'College Graduate'
            WHEN respondent_education_level IN (7, 9) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS respondent_education_level_adult,
        CASE
            WHEN respondent_education_level_detailed = 0 THEN 'Never Attended/Kindergarten'
            WHEN respondent_education_level_detailed BETWEEN 1 AND 6 THEN '1st - 6th Grade'
            WHEN respondent_education_level_detailed BETWEEN 7 AND 11  THEN '7th - 11th Grade'
            WHEN respondent_education_level_detailed = 12 THEN '12th Grade - No Diploma'
            WHEN respondent_education_level_detailed = 13 THEN 'Highschool Graduate'
            WHEN respondent_education_level_detailed = 14 THEN 'GED or Equivalent'
            WHEN respondent_education_level_detailed = 15 THEN 'More than high school'
            WHEN respondent_education_level_detailed = 55 THEN '< 5th Grade'
            WHEN respondent_education_level_detailed = 66 THEN '< 9th Grade'
            WHEN respondent_education_level_detailed IN (77, 99) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS respondent_education_level_children,
        CASE
            WHEN family_size BETWEEN 1 AND 3 THEN '1-3'
            WHEN family_size BETWEEN 4 AND 6 THEN '4-6'
            WHEN family_size = 7 THEN '7 or more'
            ELSE 'Unknown'
        END AS family_size,
        CASE
            WHEN household_size BETWEEN 1 AND 3 THEN '1-3'
            WHEN household_size BETWEEN 4 AND 6 THEN '4-6'
            WHEN household_size = 7 THEN '7 or more'
            ELSE 'Unknown'
        END AS household_size,
        children_5_or_younger AS number_of_children_5_or_younger,
        children_6_to_17 AS number_of_children_6_to_17,
        adults_60_or_older AS number_of_adults_60_or_older,
        household_head_age AS age_in_years,
        CASE
            WHEN household_head_age BETWEEN 0 AND 10 THEN '0-10'
            WHEN household_head_age BETWEEN 11 AND 20 THEN '11-20'
            WHEN household_head_age BETWEEN 21 AND 30 THEN '21-30'
            WHEN household_head_age BETWEEN 31 AND 40 THEN '31-40'
            WHEN household_head_age BETWEEN 41 AND 50 THEN '41-50'
            WHEN household_head_age BETWEEN 51 AND 60 THEN '51-60'
            WHEN household_head_age BETWEEN 61 AND 70 THEN '61-70'
            WHEN household_head_age BETWEEN 71 AND 80 THEN '71-80'
            ELSE 'Unknown'
        END AS age_group,
        CASE 
            WHEN household_head_birth_country = 1 THEN 'USA'
            WHEN household_head_birth_country = 2 THEN 'Outside USA'
            WHEN household_head_birth_country IN (77,99) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS household_head_birth_country,
        CASE
            WHEN household_head_education_level = 1 THEN '< 9th Grade'
            WHEN household_head_education_level = 2 THEN '9th - 11th Grade'
            WHEN household_head_education_level = 3 THEN 'Highschool Graduate'
            WHEN household_head_education_level = 4 THEN 'AA Degree'
            WHEN household_head_education_level = 5 THEN 'College Degree'
            WHEN household_head_education_level IN (7,9) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS household_head_education_level,
        CASE 
            WHEN household_head_gender = 1 THEN 'Male'
            WHEN household_head_gender = 2 THEN 'Female'
            ELSE 'Unknown'
        END AS household_head_gender,
        CASE 
            WHEN household_head_marital_status = 1 THEN 'Married'
            WHEN household_head_marital_status = 2 THEN 'Widowed'
            WHEN household_head_marital_status = 3 THEN 'Divorced'
            WHEN household_head_marital_status = 4 THEN 'Separated'
            WHEN household_head_marital_status = 5 THEN 'Never married'
            WHEN household_head_marital_status = 6 THEN 'Living with Partner'
            WHEN household_head_marital_status in (77,99) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS household_head_marital_status,
        CASE
            WHEN household_spouse_education_level = 1 THEN '< 9th Grade'
            WHEN household_spouse_education_level = 2 THEN '9th - 11th Grade'
            WHEN household_spouse_education_level = 3 THEN 'Highschool Graduate'
            WHEN household_spouse_education_level = 4 THEN 'AA Degree'
            WHEN household_spouse_education_level = 5 THEN 'College Degree'
            WHEN household_spouse_education_level IN (7,9) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS household_spouse_education_level,
        CASE 
            WHEN marital_status = 1 THEN 'Married'
            WHEN marital_status = 2 THEN 'Widowed'
            WHEN marital_status = 3 THEN 'Divorced'
            WHEN marital_status = 4 THEN 'Separated'
            WHEN marital_status = 5 THEN 'Never married'
            WHEN marital_status = 6 THEN 'Living with Partner'
            WHEN marital_status in (77,99) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS marital_status,
        CASE
            WHEN years_lived_in_us = 1 THEN '< 1 Yr'
            WHEN years_lived_in_us = 2 THEN '1 - 5 Yr'
            WHEN years_lived_in_us = 3 THEN '5 - 10 Yr'
            WHEN years_lived_in_us = 4 THEN '10 - 15 Yr'
            WHEN years_lived_in_us = 5 THEN '15 - 20 Yr'
            WHEN years_lived_in_us BETWEEN 6 AND 9 THEN '> 20 Yr'
            ELSE 'Unknown'
        END AS years_lived_in_us,
        CASE
            WHEN military_foreign_service = 1 THEN 'Yes'
            WHEN military_foreign_service = 2 THEN 'No'
            WHEN military_foreign_service IN (7,9) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS served_in_foreign_country,
        CASE
            WHEN fia_interpreter_used = 1 THEN 'Yes'
            WHEN fia_interpreter_used = 2 THEN 'No'
            ELSE 'Unknown'
        END AS fia_interpreter_used,
        CASE 
            WHEN fia_language_spoken = 1 THEN 'English'
            WHEN fia_language_spoken = 2 THEN 'Spanish'
            ELSE 'Unknown'
        END AS fia_language_spoken,
        CASE
            WHEN fia_proxy_respondent = 1 THEN 'Yes'
            WHEN fia_proxy_respondent = 2 THEN 'No'
            ELSE 'Unknown'
        END AS fia_proxy_respondent,
        CASE 
            WHEN family_income_range = 1 THEN '0 - 4999 USD'
            WHEN family_income_range = 2 THEN '5000 - 9999 USD'
            WHEN family_income_range = 3 THEN '10K - 14.9K USD'
            WHEN family_income_range = 4 THEN '15K - 19.9K USD'
            WHEN family_income_range = 5 THEN '20K - 24.9K USD'
            WHEN family_income_range = 6 THEN '25K - 34.9K USD'
            WHEN family_income_range = 7 THEN '35K - 44.9K USD'
            WHEN family_income_range = 8 THEN '45K - 54.9K USD'
            WHEN family_income_range = 9 THEN '55K - 64.9K USD'
            WHEN family_income_range = 10 THEN '65K - 74.9K USD'
            WHEN family_income_range = 12 THEN '> 20K USD'
            WHEN family_income_range = 14 THEN '75K - 99K USD'
            WHEN family_income_range = 15 THEN '> 100K USD'
            WHEN family_income_range IN (77,99) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS family_income_range,
        income_poverty_ratio,
        CASE 
            WHEN household_income_range = 1 THEN '0 - 4999 USD'
            WHEN household_income_range = 2 THEN '5000 - 9999 USD'
            WHEN household_income_range = 3 THEN '10K - 14.9K USD'
            WHEN household_income_range = 4 THEN '15K - 19.9K USD'
            WHEN household_income_range = 5 THEN '20K - 24.9K USD'
            WHEN household_income_range = 6 THEN '25K - 34.9K USD'
            WHEN household_income_range = 7 THEN '35K - 44.9K USD'
            WHEN household_income_range = 8 THEN '45K - 54.9K USD'
            WHEN household_income_range = 9 THEN '55K - 64.9K USD'
            WHEN household_income_range = 10 THEN '65K - 74.9K USD'
            WHEN household_income_range = 12 THEN '> 20K USD'
            WHEN household_income_range = 14 THEN '75K - 99K USD'
            WHEN household_income_range = 15 THEN '> 100K USD'
            WHEN household_income_range IN (77,99) THEN 'Refused to Answer'
            ELSE 'Unknown'
        END AS household_income_range,
        CASE
            WHEN mia_interpreter_used = 1 THEN 'Yes'
            WHEN mia_interpreter_used = 2 THEN 'No'
            ELSE 'Unknown'
        END AS mia_interpreter_used,
        CASE 
            WHEN mia_language_spoken = 1 THEN 'English'
            WHEN mia_language_spoken = 2 THEN 'Spanish'
            ELSE 'Unknown'
        END AS mia_language_spoken,
        CASE
            WHEN mia_proxy_respondent = 1 THEN 'Yes'
            WHEN mia_proxy_respondent = 2 THEN 'No'
            ELSE 'Unknown'
        END AS mia_proxy_respondent,
        CASE 
            WHEN gender = 1 THEN 'Male'
            WHEN gender = 2 THEN 'Female'
            ELSE 'Unknown'
        END AS gender,
        age_in_months_screening AS screening_age_in_months,
        age_in_years_screening AS screening_age_in_years,
        CASE
            WHEN age_in_years_screening BETWEEN 0 AND 10 THEN '0-10'
            WHEN age_in_years_screening BETWEEN 11 AND 20 THEN '11-20'
            WHEN age_in_years_screening BETWEEN 21 AND 30 THEN '21-30'
            WHEN age_in_years_screening BETWEEN 31 AND 40 THEN '31-40'
            WHEN age_in_years_screening BETWEEN 41 AND 50 THEN '41-50'
            WHEN age_in_years_screening BETWEEN 51 AND 60 THEN '51-60'
            WHEN age_in_years_screening BETWEEN 61 AND 70 THEN '61-70'
            WHEN age_in_years_screening BETWEEN 71 AND 80 THEN '71-80'
            ELSE 'Unknown'
        END AS screening_age_group_years,
        CASE
            WHEN age_in_months_screening BETWEEN 0 AND 10 THEN '< 1 Year'
            WHEN age_in_months_screening BETWEEN 11 AND 20 THEN '< 1.6 Years'
            WHEN age_in_months_screening BETWEEN 21 AND 30 THEN '1.6 Years or Older'
            ELSE 'Unknown'
        END AS screening_age_group_young,
        CASE
            WHEN exam_six_month_period = 1 THEN 'November 1 - April 30'
            WHEN exam_six_month_period = 2 THEN 'May 1 - October 31'
            ELSE 'Unknown'
        END AS exam_six_month_period,
        CASE 
            WHEN pregnancy_status = 1 THEN 'Yes'
            WHEN pregnancy_status = 2 THEN 'No'
            WHEN pregnancy_status = 3 THEN 'Not ascertain'
            ELSE 'Unknown'
        END AS pregnancy_status,
        CASE
            WHEN race_ethnicity = 1 THEN 'Mexican American'
            WHEN race_ethnicity = 2 THEN 'Other Hispanic'
            WHEN race_ethnicity = 3 THEN 'White'
            WHEN race_ethnicity = 4 THEN 'Black'
            WHEN race_ethnicity = 5 THEN 'Others'
            ELSE 'Unknown'
        END AS race_ethnicity_hispanic,
        CASE
            WHEN race_ethnicity_detailed = 1 THEN 'Mexican American'
            WHEN race_ethnicity_detailed = 2 THEN 'Other Hispanic'
            WHEN race_ethnicity_detailed = 3 THEN 'White'
            WHEN race_ethnicity_detailed = 4 THEN 'Black'
            WHEN race_ethnicity_detailed = 6 THEN 'Asian'
            WHEN race_ethnicity_detailed = 7 THEN 'Others'
            ELSE 'Unknown'
        END AS race_ethnicity_asian,
        CASE 
            WHEN participant_status = 1 THEN 'Interviewed'
            WHEN participant_status = 2 then 'Both Interviewed and MEC Examined'
            ELSE 'Unknown'
        END as participant_status,
        CASE
            WHEN sia_interpreter_used = 1 THEN 'Yes'
            WHEN sia_interpreter_used = 2 THEN 'No'
            ELSE 'Unknown'
        END AS sia_interpreter_used,
        CASE 
            WHEN sia_language_spoken = 1 THEN 'English'
            WHEN sia_language_spoken = 2 THEN 'Spanish'
            ELSE 'Unknown'
        END AS sia_language_spoken,
        CASE
            WHEN sia_proxy_respondent = 1 THEN 'Yes'
            WHEN sia_proxy_respondent = 2 THEN 'No'
            ELSE 'Unknown'
        END AS sia_proxy_respondent 
    FROM base_demographic
),

add_interview_type AS (
    SELECT *,
        COALESCE(sia_language_spoken, fia_language_spoken, mia_language_spoken) AS language_spoken,
        COALESCE(sia_interpreter_used, fia_interpreter_used, mia_interpreter_used) AS interpreter_used,
        COALESCE(sia_proxy_respondent, fia_proxy_respondent, mia_proxy_respondent) AS proxy_respondent,
        CASE 
            WHEN sia_language_spoken IS NOT NULL THEN 'sia'
            WHEN sia_interpreter_used IS NOT NULL THEN 'sia'
            WHEN sia_proxy_respondent IS NOT NULL THEN 'sia'
            WHEN fia_language_spoken IS NOT NULL THEN 'fia'
            WHEN fia_interpreter_used IS NOT NULL THEN 'fia'
            WHEN fia_proxy_respondent IS NOT NULL THEN 'fia'
            WHEN mia_language_spoken IS NOT NULL THEN 'mia'
            WHEN mia_interpreter_used IS NOT NULL THEN 'mia'
            WHEN mia_proxy_respondent IS NOT NULL THEN 'mia'
        ELSE 'Unknown'
        END AS interview_type
    FROM impute_values
),

coalesce_values AS (
    SELECT
        respondent_id,
        language,
        COALESCE(respondent_birth_country, household_head_birth_country) AS birth_country,
        respondent_us_citizen,
        COALESCE(respondent_education_level_adult, household_head_education_level) AS education_level,
        respondent_education_level_children,
        COALESCE(family_size, household_size) AS family_size,
        number_of_children_5_or_younger,
        number_of_children_6_to_17,
        number_of_adults_60_or_older,
        COALESCE(age_in_years, screening_age_in_years, screening_age_in_months/12) AS age_in_years,
        COALESCE(age_group, screening_age_group_years, screening_age_group_young) AS age_group,
        COALESCE(gender, household_head_gender) AS gender,
        COALESCE(marital_status, household_head_marital_status) AS marital_status,
        COALESCE(family_income_range, household_income_range) AS income_range,
        income_poverty_ratio,
        household_spouse_education_level,
        years_lived_in_us,
        served_in_foreign_country,
        language_spoken,
        interpreter_used,
        proxy_respondent,
        interview_type,
        exam_six_month_period,
        pregnancy_status,
        COALESCE(race_ethnicity_hispanic, race_ethnicity_asian) AS race,
        participant_status
    FROM add_interview_type
)

SELECT * FROM coalesce_values