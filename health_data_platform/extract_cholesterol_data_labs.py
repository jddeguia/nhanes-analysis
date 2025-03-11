import pandas as pd

# Load the CSV file
file_path = "labs.csv"  # Update with the actual file path
df = pd.read_csv(file_path)

# Rename relevant columns
rename_dict = {
    "SEQN": "respondent_id",
    "LBDHDD": "hdl_cholesterol_mgdl",
    "LBDHDDSI": "hdl_cholesterol_mmoll",
    "LBDTCSI": "total_cholesterol_mmoll",
    "LBXTC": "total_cholesterol_mgdl",
    "LBDSCHSI": "cholesterol_mmoll",
    "LBXSCH": "cholesterol_mgdl",
    "LBDLDL": "ldl_cholesterol_mgdl",
    "LBDLDLSI": "ldl_cholesterol_mmoll"
}

# Keep only relevant columns
df_cleaned = df[list(rename_dict.keys())].rename(columns=rename_dict)

# Save cleaned file as UTF-8
cleaned_file_path = "cholesterol_labs.csv"
df_cleaned.to_csv(cleaned_file_path, index=False, encoding="utf-8")

print(f"Cleaned CSV saved as: {cleaned_file_path}")
