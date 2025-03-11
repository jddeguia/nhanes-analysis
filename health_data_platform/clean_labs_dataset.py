import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Step 1: Scrape NHANES variable data
url = "https://wwwn.cdc.gov/Nchs/Nhanes/Search/variablelist.aspx?Component=Laboratory&CycleBeginYear=2013"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'class': 'table'})
rows = table.find_all('tr')[1:]  # Skip header row

data = []
for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 2:
        variable_name = cols[0].text.strip()
        variable_description = cols[1].text.strip()
        data.append([variable_name, variable_description])

df_nhanes = pd.DataFrame(data, columns=["Variable Name", "Variable Description"])

# Function to standardize column names
def standardize_column_name(name):
    name = name.lower().strip()
    name = re.sub(r'\s+', '_', name)  
    name = re.sub(r'[^a-z0-9_]', '', name)  
    return name

# Shorten long column names
def shorten_column_name(name, max_length=30):
    if len(name) > max_length:
        words = name.split('_')
        short_name = '_'.join(words[:3])  
        return short_name[:max_length]  
    return name

# Step 2: Load and clean labs.csv
df_labs = pd.read_csv("labs.csv", encoding="ISO-8859-1")

# Remove suffixes (.x, .y)
df_labs.columns = df_labs.columns.str.replace(r'\.[xy]$', '', regex=True)

# Replace column names using NHANES mapping
nhanes_dict = dict(zip(df_nhanes["Variable Name"], df_nhanes["Variable Description"]))
new_columns = [nhanes_dict.get(col, col) for col in df_labs.columns]

# Standardize and shorten column names
new_columns = [shorten_column_name(standardize_column_name(col)) for col in new_columns]
df_labs.columns = new_columns

# Step 3: Process medications.csv
df_medications = pd.read_csv("medications.csv", encoding="ISO-8859-1")

# Flag diabetes-related medications
diabetes_pattern = r"\bdiabet\w*\b"
df_medications["diabetes_flag"] = df_medications["RXDRSD1"].str.contains(diabetes_pattern, case=False, na=False, regex=True).astype(int)

# Drop rows where diabetes_flag is 0
df_medications = df_medications[df_medications["diabetes_flag"] == 1]

# Rename SEQN to respondent_id
df_medications = df_medications.rename(columns={"SEQN": "respondent_id"})

# Retain only relevant columns
df_medications = df_medications[["respondent_id", "diabetes_flag"]]

# Step 4: Join labs and medications data
df_merged = df_labs.merge(df_medications, how="left", left_on="respondent_sequence_number", right_on="respondent_id")

# Fill missing diabetes_flag values with 0 (i.e., those who didn't have diabetes-related medication)
df_merged["diabetes_flag"] = df_merged["diabetes_flag"].fillna(0).astype(int)

df_deduplicated = df_merged.drop_duplicates()
# Save merged dataset

df_deduplicated.to_csv("final_merged_data.csv", index=False)
print("Merged data saved to merged_data.csv")