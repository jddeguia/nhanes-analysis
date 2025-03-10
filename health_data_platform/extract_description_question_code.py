import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL of the NHANES variable list page
url = "https://wwwn.cdc.gov/Nchs/Nhanes/Search/variablelist.aspx?Component=Questionnaire&CycleBeginYear=2013"

# Send a GET request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table containing variable names and descriptions
table = soup.find('table', {'class': 'table'})

# Extract table headers and rows
rows = table.find_all('tr')[1:]  # Skip header row

# Prepare list for storing extracted data
data = []

for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 2:
        variable_name = cols[0].text.strip()
        variable_description = cols[1].text.strip()
        data.append([variable_name, variable_description])

# Create a DataFrame and save to CSV
df = pd.DataFrame(data, columns=["Variable Name", "Variable Description"])
df.to_csv("nhanes_variables.csv", index=False, encoding='utf-8')

print("Data successfully saved to nhanes_variables.csv")
