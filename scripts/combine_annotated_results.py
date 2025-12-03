import argparse
import pandas as pd 
import os
import csv

SCRIPT_DIR = os.path.dirname(__file__)

import re

import re

def clean_csv_spaces_and_empty_quotes(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:

        # 1. Remove spaces AFTER commas before a quote
        #    ,   "value"  → ,"value"
        line = re.sub(r',\s+"', ',"', line)

        # 2. Remove spaces AFTER commas before a non-quote character
        #    ,   value  → ,value
        line = re.sub(r',\s+([^"])', r',\1', line)

        # 3. Remove spaces BEFORE commas
        #    value   ,next → value,next
        line = re.sub(r'\s+,', ',', line)

        # 4. Replace empty quoted strings "" → empty field
        #    ,"", → ,,
        line = line.replace('""', '')

        cleaned_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    print("Finished cleaning CSV →", output_path)


def main():
    df1 = pd.read_csv(os.path.join(SCRIPT_DIR, "..", "data", "open_coding_articles.tsv"), index_col=0, sep="\t")

    '''
    clean_csv_spaces_and_empty_quotes(
        os.path.join(SCRIPT_DIR, "..", "data", "articles", "remaining_articles_group1.csv"),
        os.path.join(SCRIPT_DIR, "..", "data", "articles", "remaining_articles_group1_cleaned.csv")
    )
    '''

    df2 = pd.read_csv(os.path.join(SCRIPT_DIR, "..", "data", "articles", "remaining_articles_group1_cleaned.csv"), index_col="index")
    df3 = pd.read_csv(os.path.join(SCRIPT_DIR, "..", "data", "articles", "remaining_articles_group2.csv"), index_col="index")
    df4 = pd.read_csv(os.path.join(SCRIPT_DIR, "..", "data", "articles", "remaining_articles_group3.csv"), index_col="index")

    combined = pd.concat([df1, df2, df3, df4], ignore_index=False)
    combined = combined.sort_index()
    combined.to_csv(os.path.join(SCRIPT_DIR, "..", "data", "articles", "final_annotated_articles.tsv"), sep="\t")

if __name__ == "__main__":
    main()