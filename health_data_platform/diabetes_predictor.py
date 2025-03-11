import pandas as pd
import numpy as np
import logging
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Progress Bar
steps = [
    "Loading dataset", "Selecting numeric columns", "Handling missing values",
    "Defining features & target", "Splitting data", "Applying SMOTE",
    "Scaling features", "Selecting top features", "Training model",
    "Making predictions", "Evaluating model"
]
pbar = tqdm(total=len(steps), desc="Progress", ncols=100, bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} steps")


def load_data(filepath: str) -> pd.DataFrame:
    """Loads the dataset from a CSV file."""
    logging.info("Loading dataset...")
    df = pd.read_csv(filepath)
    pbar.update(1)
    return df


def preprocess_data(df: pd.DataFrame, target_col: str):
    """Prepares the dataset by selecting numeric columns and handling missing values."""
    logging.info("Selecting only numeric columns...")
    df = df.select_dtypes(include=[np.number])
    pbar.update(1)

    logging.info("Handling missing values (filling with median)...")
    df.fillna(df.median(), inplace=True)
    pbar.update(1)

    logging.info("Defining features and target variable...")
    X = df.drop(columns=[target_col])
    y = df[target_col]
    pbar.update(1)

    return X, y


def split_data(X, y, test_size=0.2):
    """Splits the dataset into training and testing sets."""
    logging.info("Splitting data into training and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)
    pbar.update(1)
    return X_train, X_test, y_train, y_test


def apply_smote(X_train, y_train):
    """Applies SMOTE to balance the dataset."""
    logging.info("Applying SMOTE to balance dataset...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    pbar.update(1)
    return X_train_resampled, y_train_resampled


def scale_features(X_train, X_test):
    """Scales features using StandardScaler."""
    logging.info("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    pbar.update(1)
    return X_train_scaled, X_test_scaled


def select_top_features(X_train, y_train, X_test, top_n=10):
    """Selects the top N most important features using Logistic Regression coefficients."""
    logging.info(f"Selecting top {top_n} features based on Logistic Regression coefficients...")
    base_model = LogisticRegression(max_iter=1000, solver="lbfgs")
    base_model.fit(X_train, y_train)

    feature_importance = np.abs(base_model.coef_).flatten()
    top_features_idx = np.argsort(feature_importance)[-top_n:]

    X_train_selected = X_train[:, top_features_idx]
    X_test_selected = X_test[:, top_features_idx]
    pbar.update(1)

    return X_train_selected, X_test_selected


def train_model(X_train, y_train):
    """Trains a Logistic Regression model."""
    logging.info("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, solver="lbfgs")
    model.fit(X_train, y_train)
    pbar.update(1)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluates the model and logs the results."""
    logging.info("Making predictions...")
    y_pred = model.predict(X_test)
    pbar.update(1)

    logging.info("Evaluating model...")
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    pbar.update(1)

    logging.info(f"\n Model Accuracy: {accuracy:.4f}")
    logging.info(f"\n Classification Report:\n{report}")

    print("\n📊 Final Results:")
    print("Model Accuracy:", accuracy)
    print("Classification Report:\n", report)


# --- Execution Flow ---
df = load_data("final_merged_data.csv")
X, y = preprocess_data(df, target_col="diabetes_flag")
X_train, X_test, y_train, y_test = split_data(X, y)
X_train_resampled, y_train_resampled = apply_smote(X_train, y_train)
X_train_scaled, X_test_scaled = scale_features(X_train_resampled, X_test)
X_train_selected, X_test_selected = select_top_features(X_train_scaled, y_train_resampled, X_test_scaled, top_n=10)
model = train_model(X_train_selected, y_train_resampled)
evaluate_model(model, X_test_selected, y_test)

pbar.close()
