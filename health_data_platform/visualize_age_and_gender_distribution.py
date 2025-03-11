import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to DuckDB database
conn = duckdb.connect(database='./dev.duckdb', read_only=False)

# Load gender and age_group data from mart_demographic
query = """
    SELECT gender, age_group, COUNT(*) AS count
    FROM mart_demographic
    GROUP BY gender, age_group
    ORDER BY age_group
"""
df = conn.execute(query).df()

# Close the connection
conn.close()

# Set seaborn style
sns.set_style("whitegrid")

# Create subplots (1 row, 2 columns)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Bar chart: Age group distribution (ignoring gender)
sns.barplot(x="age_group", y="count", data=df.groupby("age_group", as_index=False).sum(), palette="Blues", ax=axes[0])
axes[0].set_title("Distribution by Age Group")
axes[0].set_xlabel("Age Group")
axes[0].set_ylabel("Number of Respondents")
axes[0].tick_params(axis='x', rotation=45)

# Bar chart: Gender distribution within each age group
sns.barplot(x="age_group", y="count", hue="gender", data=df, palette="coolwarm", ax=axes[1])
axes[1].set_title("Gender Distribution by Age Group")
axes[1].set_xlabel("Age Group")
axes[1].set_ylabel("Number of Respondents")
axes[1].tick_params(axis='x', rotation=45)
axes[1].legend(title="Gender")

# Adjust layout
plt.tight_layout()

output_path = "gender_age_distribution.png"
plt.savefig(output_path, dpi=300)  # High resolution

print(f"Plot saved as {output_path}")