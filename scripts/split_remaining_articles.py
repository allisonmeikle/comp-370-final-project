import pandas as pd
import random

# Set random seed for reproducibility
random.seed(42)

# Read the CSV file with all articles
csv_file = '../data/articles/articles_final_fixed.csv'
df_all = pd.read_csv(csv_file)

print(f"Total articles in CSV: {len(df_all)}")

tsv_file = '../data/open_coding_articles.tsv'
df_annotated = pd.read_csv(tsv_file, sep='\t', quoting=3)

# Get the indices from the first column 
annotated_indices = df_annotated.iloc[:, 0].tolist()

# Get all indices from the CSV
all_indices = list(range(len(df_all)))

# Find remaining indices
remaining_indices = [i for i in all_indices if i not in annotated_indices]

# Verify we have exactly 300 remaining
assert len(remaining_indices) == 300, f"Expected 300 remaining articles, got {len(remaining_indices)}"

# Shuffle the remaining indices randomly
random.shuffle(remaining_indices)

# Split into 3 groups of 100 each
group1_indices = remaining_indices[0:100]
group2_indices = remaining_indices[100:200]
group3_indices = remaining_indices[200:300]

# Create dataframes for each group
df_group1 = df_all.iloc[group1_indices].copy()
df_group2 = df_all.iloc[group2_indices].copy()
df_group3 = df_all.iloc[group3_indices].copy()

# Add the original index as the first column
df_group1.insert(0, 'index', group1_indices)
df_group2.insert(0, 'index', group2_indices)
df_group3.insert(0, 'index', group3_indices)

# Save to new CSV files
output_dir = '../data/articles/'
df_group1.to_csv(f'{output_dir}remaining_articles_group1.csv', index=False)
df_group2.to_csv(f'{output_dir}remaining_articles_group2.csv', index=False)
df_group3.to_csv(f'{output_dir}remaining_articles_group3.csv', index=False)

print("\nSuccessfully created 3 CSV files:")
print(f"- remaining_articles_group1.csv: {len(df_group1)} articles")
print(f"- remaining_articles_group2.csv: {len(df_group2)} articles")
print(f"- remaining_articles_group3.csv: {len(df_group3)} articles")

# Verify no overlap between groups
all_split_indices = set(group1_indices + group2_indices + group3_indices)
print(f"\nVerification:")
print(f"Total unique articles in 3 groups: {len(all_split_indices)}")
print(f"All 300 remaining articles covered: {len(all_split_indices) == 300}")
print(f"No overlap with annotated articles: {len(all_split_indices.intersection(set(annotated_indices))) == 0}")
