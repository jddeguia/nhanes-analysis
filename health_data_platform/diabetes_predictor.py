import pandas as pd
import numpy as np
import logging
from tqdm import tqdm  # Progress bar
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Progress bar steps
steps = [
    "Loading dataset",
    "Selecting numeric columns",
    "Handling missing values",
    "Defining features & target",
    "Splitting data",
    "Applying SMOTE",
    "Scaling features",
    "Selecting top features",
    "Training Logistic Regression",
    "Making predictions",
    "Evaluating model"
]
pbar = tqdm(total=len(steps), desc="Progress", ncols=100, bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} steps")

# 1. Load dataset
logging.info("Loading dataset...")
df = pd.read_csv("final_merged_data.csv")  # Replace with actual file
pbar.update(1)

# 2. Drop non-numeric columns
logging.info("Selecting only numeric columns...")
df = df.select_dtypes(include=[np.number])
pbar.update(1)

# 3. Handle missing values
logging.info("Handling missing values by filling with median...")
df.fillna(df.median(), inplace=True)
pbar.update(1)

# 4. Define features and target
logging.info("Defining features and target variable...")
X = df.drop(columns=["diabetes_flag"])  # Replace with actual target column
y = df["diabetes_flag"]
pbar.update(1)

# 5. Split data
logging.info("Splitting data into training and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
pbar.update(1)

# 6. Apply SMOTE
logging.info("Applying SMOTE to balance dataset...")
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
pbar.update(1)

# 7. Scale features
logging.info("Scaling features using StandardScaler...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)
pbar.update(1)

# 8. Feature Selection using Logistic Regression Coefficients
logging.info("Selecting top features based on Logistic Regression coefficients...")
base_model = LogisticRegression(max_iter=1000, solver="lbfgs")
base_model.fit(X_train_scaled, y_train_resampled)

# Get feature importance (absolute values)
feature_importance = np.abs(base_model.coef_).flatten()
top_features_idx = np.argsort(feature_importance)[-10:]  # Select top 10 features
X_train_selected = X_train_scaled[:, top_features_idx]
X_test_selected = X_test_scaled[:, top_features_idx]
pbar.update(1)

# 9. Train Logistic Regression model
logging.info("Training Logistic Regression model with selected features...")
model = LogisticRegression(max_iter=1000, solver="lbfgs")
model.fit(X_train_selected, y_train_resampled)
pbar.update(1)

# 10. Make predictions
logging.info("Making predictions...")
y_pred = model.predict(X_test_selected)
pbar.update(1)

# 11. Evaluate model
logging.info("Evaluating model...")
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
pbar.update(1)

pbar.close()

# Print results
logging.info(f"Model Accuracy: {accuracy:.4f}")
logging.info(f"Classification Report:\n{report}")

print("\n Final Results:")
print("Model Accuracy:", accuracy)
print("Classification Report:\n", report)
