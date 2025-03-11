import duckdb

# Connect to the DuckDB database
conn = duckdb.connect(database='./dev.duckdb', read_only=False)


table_name = "mart_private_health_insurance_by_age_group"  # Change this to any table you want to preview
preview_query = f"SELECT * FROM {table_name} ORDER BY 1"
preview_data = conn.execute(preview_query).df()
print(f"\nQuery Result:")
print(preview_data)

conn.close()
