import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Constants
NHANES_URL = "https://wwwn.cdc.gov/Nchs/Nhanes/Search/variablelist.aspx?Component=Laboratory&CycleBeginYear=2013"
LABS_FILE = "labs.csv"
MEDICATIONS_FILE = "medications.csv"
OUTPUT_FILE = "final_merged_data.csv"

# Function to scrape NHANES variable data
def scrape_nhanes_variable_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "table"})

    if not table:
        raise ValueError("No table found on the NHANES page.")

    rows = table.find_all("tr")[1:]  # Skip header row
    data = [[col.text.strip() for col in row.find_all("td")[:2]] for row in rows if len(row.find_all("td")) >= 2]

    return pd.DataFrame(data, columns=["Variable Name", "Variable Description"])

# Function to standardize and shorten column names
def clean_column_name(name, max_length=30):
    """ Standardize and shorten column names """
    name = re.sub(r"\s+", "_", name.strip().lower())  # Replace spaces with underscores
    name = re.sub(r"[^a-z0-9_]", "", name)  # Remove special characters
    return name[:max_length] if len(name) > max_length else name  # Shorten if necessary

# Function to clean and map lab data
def clean_labs_data(df, nhanes_dict):
    if "SEQN" not in df.columns:
        raise ValueError("Missing 'SEQN' column in labs file.")

    df.rename(columns={"SEQN": "respondent_sequence_number"}, inplace=True)
    df.columns = df.columns.str.replace(r"\.[xy]$", "", regex=True)  # Remove suffixes (.x, .y)
    df.columns = [clean_column_name(nhanes_dict.get(col, col)) for col in df.columns]  # Map and clean column names
    return df

# Function to process medications data
def process_medications_data(df):
    if "SEQN" not in df.columns or "RXDRSD1" not in df.columns:
        raise ValueError("Missing required columns in medications file.")

    diabetes_pattern = r"\bdiabet\w*\b"
    df["diabetes_flag"] = df["RXDRSD1"].str.contains(diabetes_pattern, case=False, na=False, regex=True).astype(int)
    df = df[df["diabetes_flag"] == 1][["SEQN", "diabetes_flag"]]  # Keep only relevant data
    df.rename(columns={"SEQN": "respondent_id"}, inplace=True)
    return df

# Function to merge datasets
def merge_data(df_labs, df_medications):
    if "respondent_sequence_number" not in df_labs.columns:
        raise ValueError("Missing 'respondent_sequence_number' column in lab data.")

    df_merged = df_labs.merge(df_medications, how="left", left_on="respondent_sequence_number", right_on="respondent_id")

    # Fill missing diabetes_flag values with 0
    df_merged["diabetes_flag"] = df_merged["diabetes_flag"].fillna(0).astype(int)

    # Drop respondent_id since it's redundant after merging
    return df_merged.drop(columns=["respondent_id"], errors="ignore").drop_duplicates()

# Main execution
try:
    # Scrape NHANES variable data
    df_nhanes = scrape_nhanes_variable_data(NHANES_URL)
    nhanes_dict = dict(zip(df_nhanes["Variable Name"], df_nhanes["Variable Description"]))

    # Load and clean lab data
    df_labs = clean_labs_data(pd.read_csv(LABS_FILE, encoding="ISO-8859-1"), nhanes_dict)

    # Load and process medications data
    df_medications = process_medications_data(pd.read_csv(MEDICATIONS_FILE, encoding="ISO-8859-1"))

    # Merge and save final dataset
    df_final = merge_data(df_labs, df_medications)
    df_final.to_csv(OUTPUT_FILE, index=False)

    print(f"Merged data saved to {OUTPUT_FILE}")

except Exception as e:
    print(f"Error: {e}")
