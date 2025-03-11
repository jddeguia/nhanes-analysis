import pandas as pd

# Load the dataset
file_path = "medications.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Drop rows where RXDDRUG contains numbers or is NaN
df = df[~df['RXDDRUG'].astype(str).str.contains(r'\d', regex=True, na=False)]
df['RXDDRUG'].fillna("NO PRESCRIBED MEDICATIONS", inplace=True)

# Combine RXDRSD1, RXDRSD2, RXDRSD3 into a list (excluding NaNs)
df['RXDRSD'] = df[['RXDRSD1', 'RXDRSD2', 'RXDRSD3']].apply(lambda x: [i for i in x if pd.notna(i)], axis=1)

# Combine RXDRSC1, RXDRSC2, RXDRSC3 into a list (excluding NaNs)
df['RXDRSC'] = df[['RXDRSC1', 'RXDRSC2', 'RXDRSC3']].apply(lambda x: [i for i in x if pd.notna(i)], axis=1)

# Drop original columns now that they are merged
df = df.drop(columns=['RXDRSD1', 'RXDRSD2', 'RXDRSD3', 'RXDRSC1', 'RXDRSC2', 'RXDRSC3'])

# Aggregate data to have unique SEQN per row
df_grouped = df.groupby("SEQN").agg({
    "RXDDRUG": lambda x: list(x.unique()) if len(x.unique()) > 0 else ["NO PRESCRIBED MEDICATIONS"],
    "RXDRSD": lambda x: list(set(sum(x, []))) if len(set(sum(x, []))) > 0 else ["N/A"],
    "RXDRSC": lambda x: list(set(sum(x, []))) if len(set(sum(x, []))) > 0 else ["N/A"]
}).reset_index()

# Rename columns
df_grouped.rename(columns={
    "SEQN": "respondent_id",
    "RXDDRUG": "generic_drug_name_list",
    "RXDRSD": "medication_list",
    "RXDRSC": "medication_code"
}, inplace=True)

# Save the cleaned dataset
output_file = "medications_cleaned.csv"
df_grouped.to_csv(output_file, index=False, encoding="utf-8")
print(f"Cleaned dataset saved as {output_file}")
