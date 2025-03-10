import duckdb

# Connect to the DuckDB database
conn = duckdb.connect(database='./dev.duckdb', read_only=False)

# Show present tables
tables = conn.execute("SHOW TABLES").fetchall()
print("Tables in DuckDB:")
for table in tables:
    print(table[0])

# Preview first 5 rows of a specific table
table_name = "base_health_insurance_questionnaire"  # Change this to any table you want to preview
preview_query = f"SELECT * FROM {table_name} WHERE response IS NOT NULL"
preview_data = conn.execute(preview_query).df()
print(f"\nFirst 5 rows of {table_name}:")
print(preview_data)

conn.close()
