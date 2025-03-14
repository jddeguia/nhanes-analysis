import duckdb

# Connect to the DuckDB database
conn = duckdb.connect(database='./dev.duckdb', read_only=False)

# List of tables to query
tables = [
    "mart_demographic"
]

# Loop through each table and export its data to a CSV file
for table in tables:
    query = f"SELECT * FROM {table}"
    output_file = f"{table}.csv"
    # Execute the query and save the result to a CSV file
    conn.execute(query).df().to_csv(output_file, index=False)
    print(f"Data exported to {output_file}")

# Close the connection
conn.close()