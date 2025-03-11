import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

# Load your dataset
df = pd.read_csv("final_merged_data.csv")  # Replace with actual file

# Drop non-numeric columns (or encode them properly if needed)
df = df.select_dtypes(include=[np.number])

# Handle missing values (fill with median)
df.fillna(df.median(), inplace=True)

# Define features and target
X = df.drop(columns=["diabetes_flag"])  # Replace with actual target column
y = df["diabetes_flag"]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000, solver="lbfgs")
model.fit(X_train_scaled, y_train_resampled)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate model
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
