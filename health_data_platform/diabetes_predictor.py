import pandas as pd
import numpy as np
import logging
from tqdm import tqdm
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
from imblearn.over_sampling import SMOTE

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load dataset
def load_data(filepath: str) -> pd.DataFrame:
    logging.info("Loading dataset...")
    return pd.read_csv(filepath)

def preprocess_data(df: pd.DataFrame, target_col: str):
    logging.info("Preprocessing dataset...")
    df = df.select_dtypes(include=[np.number])  # Keep only numerical features
    df.fillna(df.median(), inplace=True)  # Fill missing values with median
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y

# Load and preprocess dataset
df = load_data("final_merged_data.csv")
X, y = preprocess_data(df, target_col="diabetes_flag")

# Stratified K-Fold setup
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
accuracy_scores = []
f1_scores = []
all_reports = []

# Progress bar for cross-validation
for fold, (train_idx, test_idx) in enumerate(tqdm(kf.split(X, y), total=kf.get_n_splits(), desc="Cross-validation Progress"), 1):
    logging.info(f"Processing Fold {fold}...")

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    # Apply SMOTE only on training data
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_resampled)
    X_test_scaled = scaler.transform(X_test)

    # Feature Selection using Random Forest
    logging.info("Selecting top 15 features using Random Forest...")
    feature_selector = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    feature_selector.fit(X_train_scaled, y_train_resampled)

    feature_importance = feature_selector.feature_importances_
    top_features_idx = np.argsort(feature_importance)[-15:]  # Select top 15 features

    X_train_selected = X_train_scaled[:, top_features_idx]
    X_test_selected = X_test_scaled[:, top_features_idx]

    # Train ensemble model using Bagging with Random Forest
    base_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    ensemble_model = BaggingClassifier(base_model, n_estimators=15, bootstrap=True, random_state=42, n_jobs=-1)
    ensemble_model.fit(X_train_selected, y_train_resampled)

    # Evaluate model
    y_pred = ensemble_model.predict(X_test_selected)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")  # Use macro-average for class balance
    report = classification_report(y_test, y_pred)
    
    accuracy_scores.append(accuracy)
    f1_scores.append(f1)
    all_reports.append(report)
    
    logging.info(f"Fold {fold} Accuracy: {accuracy:.4f}")
    logging.info(f"Fold {fold} F1-score: {f1:.4f}")
    logging.info(f"Fold {fold} Classification Report:\n{report}")

# Final evaluation summary
logging.info("\n📊 Cross-Validation Results:")
logging.info(f"Average Accuracy: {np.mean(accuracy_scores):.4f}")
logging.info(f"Average F1-score: {np.mean(f1_scores):.4f}")
