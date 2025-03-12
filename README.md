# Detailed Summary of Workflow (for answering queries)

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

# Diabetes Prediction Model: Workflow & Results
![diabetes_prediction_flowchart](https://github.com/user-attachments/assets/8105aa62-5b5a-4352-8e16-e7ff656c2fcd)


## 1. Data Loading and Preprocessing
- The merged dataset is loaded.
- Only **numerical columns** are retained.
- **Missing values** are imputed using the **median**.
- The dataset is split into:
  - **Features (X)**
  - **Target variable (y)** – indicating diabetes presence.

## 2. Cross-Validation with Stratified K-Fold
- **5-fold Stratified K-Fold cross-validation** ensures class balance across folds.
- For each fold:
  1. The dataset is split into **training** and **testing** sets.
  2. **SMOTE** is applied to balance class distribution in the training set.
  3. **StandardScaler** is used for **feature scaling**.

## 3. Feature Selection
- A **Random Forest model** selects the **top 15 most important features**.
- These features are used for training and testing.

## 4. Model Training and Evaluation
- A **BaggingClassifier** with a **Random Forest base model** is trained.
- Predictions are made on the test set.
- **Evaluation metrics include:**
  - **Accuracy score**
  - **Macro-averaged F1 score**
  - **Classification report**

## 5. Summary of Results

### Diabetes Prediction Model: Cross-Validation Results
Our diabetes prediction model was evaluated using **5-fold cross-validation**, leveraging a **Random Forest classifier** for feature selection and classification.

### Top 15 Most Important Features
The most influential features across all folds include:
1. **Glycohemoglobin (HbA1c)** – most important predictor
2. **Glucose (Refrigerated Serum, mmol/L & mg/dL)** – second most important
3. **Osmolality (mmol/kg)**
4. **Albumin-Creatinine Ratio (mg/g)**
5. **Triglycerides (Refrigerated, mmol/L & mg/dL)**
6. **Basophils Count (per 1000 cells/µL)**
7. **Blood Urea Nitrogen (BUN, mg/dL & mmol/L)**
8. **Albumin (g/dL, g/L, and Urine mg/L)**
9. **Incomplete OGTT Comment Code**

### Performance Metrics
| Fold | Accuracy  | F1-score (Diabetic Class) | Precision (Diabetic Class) | Recall (Diabetic Class) |
|------|----------|--------------------------|----------------------------|--------------------------|
| 1    | 95.52%   | 0.8319                   | 0.60                       | 0.81                     |
| 2    | 94.75%   | 0.8124                   | 0.55                       | 0.81                     |
| 3    | 94.75%   | 0.8052                   | 0.55                       | 0.76                     |
| 4    | 96.69%   | -                         | -                           | -                         |
| 5    | Pending  | Pending                   | Pending                     | Pending                   |

### Key Observations
- The model **performs well** in distinguishing **diabetic vs. non-diabetic** cases, achieving an **average accuracy of ~95%**.
- The **recall for the diabetic class (~76-81%)** suggests the model effectively identifies diabetic cases but still **misses some**.
- The **precision for the diabetic class (55-60%)** indicates **some false positives**.
- **Feature importance analysis** consistently ranks **glycohemoglobin and glucose levels** as the **strongest predictors**.
