{{
    config(
      materialized='table'
    )
}}

{% set column_types = {
    'respondent_id': 'string',
    'hdl_cholesterol_mgdl': 'integer',
    'hdl_cholesterol_mmoll': 'float',
    'total_cholesterol_mmoll': 'float',
    'total_cholesterol_mgdl': 'integer',
    'cholesterol_mmoll': 'float',
    'cholesterol_mgdl': 'integer',
    'ldl_cholesterol_mgdl' : 'integer',
    'ldl_cholesterol_mmoll' : 'float'
} %}

{% set columns = ['respondent_id', 'hdl_cholesterol_mgdl', 'hdl_cholesterol_mmoll', 
'total_cholesterol_mmoll', 'total_cholesterol_mgdl', 'cholesterol_mmoll', 'cholesterol_mgdl',
'ldl_cholesterol_mgdl', 'ldl_cholesterol_mmoll'] %}

WITH cholesterol_labs_base AS (
    SELECT * 
    FROM {{ ref('cholesterol_labs') }}
),

cast_data_type AS (
    SELECT
        {% for column in columns %}
            {% set data_type = column_types[column] %}
            {% if loop.index > 1 %}, {% endif %}
            {% if data_type == 'string' %}
                CAST({{ column }} AS VARCHAR) AS {{ column }}
            {% elif data_type == 'integer' %}
                CAST({{ column }} AS INT) AS {{ column }}
            {% elif data_type == 'float' %}
                CAST({{ column }} AS FLOAT) AS {{ column }}
            {% elif data_type == 'date' %}
                TRY_CAST(STRPTIME({{ column }}, '%d/%m/%Y') AS DATE) AS {{ column }}
            {% else %}
                {{ column }} AS {{ column }}
            {% endif %}
        {% endfor %}
    FROM cholesterol_labs_base
)

SELECT *
FROM cast_data_type