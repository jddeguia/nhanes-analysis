# Detailed Summary of Workflow

![image](https://github.com/user-attachments/assets/55016c92-9f0b-4c2a-b61a-94f106cd4d2e)

## 1. Data Extraction
A Python script extracts NHANES questionnaire variable names and descriptions from an online source.

### Process:
- Fetches webpage content using `requests`.
- Parses HTML to locate the relevant table with `BeautifulSoup`.
- Extracts variable names and descriptions and saves them for reference.
- The extracted data is used to map question codes to their definitions in dbt models.

## 2. Base Layer (dbt Processing)
- Loads raw questionnaire data from the source database by using dbt seed
- Integrates metadata by mapping question codes to definitions.
- Ensures each record contains:
  - **Respondent ID** (unique identifier)
  - **Question Code** (survey question identifier)
  - **Response** (raw data)
  - **Question Type** (categorization)
  - **Definition** (human-readable description)

## 3. Staging Layer (Data Transformation & Standardization)
Enhances the dataset by:
- **Adding Short Definitions:** Assigns human-friendly labels to question codes (e.g., `HIQ031C` → `is_covered_by_medigap`).
- **Standardizing Responses:** Maps raw responses to meaningful values, such as:
  - `1` → **Yes**, `2` → **No**, `7/9` → **Refused**.
  - Unmapped responses default to `No` or `Unknown`.
- Produces a structured dataset with cleaned responses and easy-to-understand column names.

## 4. Mart Layer (Aggregations & Analysis)
- Merges demographic data with health insurance responses.
- Aggregates insurance coverage statistics by gender.
- Uses SQL calculations to count respondents with and without coverage.

## 5. Validation & Testing
- Uses **DuckDB** for ad hoc testing of dbt models before deployment.
- Ensures:
  - All question codes are correctly mapped.
  - Extracted metadata aligns with dbt outputs.
  - Data integrity and consistency checks pass.

## 6. Final Deliverables
- **Reference Data:** Extracted questionnaire metadata.
- **Processed dbt Models:** Cleaned and structured data ready for analysis.
- **Aggregated Reports:** Insights into health insurance coverage trends.
