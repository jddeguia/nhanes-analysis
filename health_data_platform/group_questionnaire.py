import pandas as pd

# Load dataset
df = pd.read_csv("questionnaire.csv")

# Define a mapping of prefixes to question types
question_mapping = {
    "DLQ": "Disability",
    "DED": "Dermatology",
    "OSD": "Osteoporosis",
    "OSQ": "Osteoporosis",
    "IMQ": "Immunization",
    "SXD": "Sexual Behavior",
    "SXQ": "Sexual Behaivor",
    "CDQ": "Cardiovascular Health",
    "BPD": "Blood Pressure & Cholesterol",
    "BPQ": "Blood Pressure & Cholesterol",
    "AGQ": "Medical Conditions",
    "MCD": "Medical Conditions",
    "MCQ": "Medical Conditions",
    "HIQ": "Health Insurance",
    "HUD": "Hospital Utilization & Access to Care",
    "HUQ": "Hospital Utilization & Access to Care",
    "PAA": "Physical Activity",
    "PAD": "Physical Activity",
    "PAQ": "Physical Activity",
    "PFQ": "Physical Functioning",
    "HEQ": "Hepatitis",
    "ECD": "Early Childhood",
    "WHQ": "Early Childhood",
    "DID": "Diabetes",
    "DIQ": "Diabetes",
    "SMD": "Smoking",
    "SMQ": "Smoking",
    "SMA": "Smoking",
    "HOD": "Housing Characteristics",
    "HOQ": "Housing Characteristics",
    "PUQ": "Pesticide Use",
    "IND": "Income",
    "INQ": "Income",
    "AUQ": "Taste & Smell",
    "CSQ": "Taste & Smell",
    "CBQ": "Diet Behavior & Nutrition",
    "DBD": "Diet Behavior & Nutrition",
    "DBQ": "Diet Behavior & Nutrition",
    "CBD": "Consumer Behavior",
    "HSA": "Current Health Status",
    "HSD": "Current Health Status",
    "HSQ": "Current Health Status",
    "SLD": "Sleep Disorders",
    "RXD": "Preventive Aspirin Use",
    "RXQ": "Preventive Aspirin Use",
    "DUQ": "Drug Use",
    "WHQ": "Weight History",
    "WHD": "Weight History",
    "ALQ": "Alcohol Use",
    "ALD": "Alcohol Use",
    "DPQ": "Mental Health",
    "ACD": "Acculturation",
    "RHD": "Reproductive Health",
    "RHQ": "Reproductive Health",
    "FSD": "Food Security",
    "FSQ": "Food Security",
    "OHQ": "Oral Health",
    "OCD": "Occupation",
    "RXD": "Prescription Medications",
    "RXQ": "Prescription Medications",
    "KID": "Kidney Conditions",
    "KIQ": "Kidney Conditions",
    "CKD": "Creatine Kinase",
    "CKQ": "Creatine Kinase",
    "VTQ": "Volatile Toxicant",
    "WTS": "Volatile Toxicant",
    "CFA": "Cognitive Functioning",
    "CFD": "Cognitive Functioning",
    # Add more prefixes if needed
}

# Function to classify columns based on prefix
def classify_column(col_name):
    prefix = col_name[:3]  # Extract first 3 characters
    return question_mapping.get(prefix, "Other")  # Default to "Other" if not mapped

# Create a dictionary mapping column names to question types
column_classification = {col: classify_column(col) for col in df.columns}

# 🔹 Unpivot (melt) the dataset
df_long = df.melt(id_vars=["SEQN"], var_name="question_code", value_name="response")

# 🔹 Add question type based on the mapping
df_long["question_type"] = df_long["question_code"].map(column_classification)

# 🔹 Export separate CSV files for each question type
for question_type, group_df in df_long.groupby('question_type'):
    output_file = f"questionnaire_{question_type.replace(' ', '_')}.csv"
    group_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"✅ {question_type} data saved to: {output_file}")


