import pandas as pd

print("Data manipulation...")

data = pd.read_excel('data/intermediate/WT25_notes_cleaned.xlsx')
cols = data.select_dtypes(include=["float64"]).columns
crit = [c for c in cols if not c.__contains__('Total')]

# Data long format
data_long = data.melt(id_vars=('Spinner', 'Round', 'Judge'), value_vars=crit, var_name='Criterion', value_name='Score')

# Z-Score Normalization
data_long['Z-Score'] = data_long.groupby(['Criterion', 'Judge'])['Score'].transform(lambda x: (x - x.mean()) / x.std(ddof=0))

# Save manipulated data
data_long.to_excel('data/intermediate/WT25_notes_long.xlsx', index=False)