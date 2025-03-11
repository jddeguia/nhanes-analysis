import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, accuracy_score

# Load data
df = pd.read_csv("final_merged_data.csv")

# Drop duplicate columns
df = df.loc[:, ~df.columns.duplicated()]

# Define target variable
target_col = "diabetes_flag"
if target_col not in df.columns:
    raise ValueError(f"Target column '{target_col}' not found in dataset!")

# Separate features and target
X = df.drop(columns=[target_col])
y = df[target_col]

# Drop columns that may cause encoding issues
drop_cols = ["respondent_sequency_number","gender", "race", "pregnancy_status"]
X = X.drop(columns=[col for col in drop_cols if col in X.columns], errors="ignore")

# Encode categorical variables
cat_cols = X.select_dtypes(include=["object"]).columns
if len(cat_cols) > 0:
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le

# Handle missing values with median
imputer = SimpleImputer(strategy="median")
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)


# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

print(X.corrwith(y).sort_values(ascending=False))  # Shows correlation with target