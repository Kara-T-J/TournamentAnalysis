import pandas as pd

data_raw = pd.read_excel('data/source/WT25_notes_raw.xlsx')

print("Data preparation...")

# Cleaning folder structure
import os
for folder in ['data/intermediate', 'data/result']:
    os.makedirs(folder, exist_ok=True)
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        if os.path.isfile(file_path):
            os.remove(file_path)


# Check file format and structure
columns_names = data_raw.columns.tolist()

if columns_names.__contains__('Spinner') and columns_names.__contains__('Round'):
    if data_raw['Spinner'].dtype == 'object' and data_raw['Judge'].dtype == 'object' and data_raw['Round'].dtype == 'int64':
        cols = data_raw.select_dtypes(include=["float64"]).columns
        crit = [c for c in cols if not c.__contains__('Total')]
    else:
        raise ValueError("Data types are incorrect. 'Spinner' should be of type object and 'Round' should be of type int64.")
else:
    raise ValueError("File format is incorrect. Expected columns 'Spinner' and/or 'Round' not found.")

# Remove NaN, duplicates, and irrelevant values
data_nonan = data_raw.dropna(subset=crit, how='all')
data_nodup = data_nonan.drop_duplicates()
data_cleaned = data_nodup[data_nodup['Total'] > 0]

# Save cleaned data
data_cleaned.to_excel('data/intermediate/WT25_notes_cleaned.xlsx', index=False)
print("... done without error.")