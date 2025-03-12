# dbt Project Overview
![dbt_project_flowchart](https://github.com/user-attachments/assets/ffb5ffc9-86b7-4dba-bd26-d94f25c08944)


## 1. Base Layer
- Exposes **static data** to the dbt project using **dbt seed**.

## 2. Staging Layer
- **Casting explicit data types** to ensure consistency.
- **Renaming columns** for better readability.
- **Mapping values** to standardized formats.

## 3. Mart Layer
- Exposes data to **DuckDB** for analysis and validation.
