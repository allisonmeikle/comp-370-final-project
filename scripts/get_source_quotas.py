import argparse
import numpy as np
import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(__file__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str, help="Path to input data file")
    args = parser.parse_args()

    num_articles = 500
    filename = args.data

    df = pd.read_csv(filename)

    df['visits'] = pd.to_numeric(df['visits'], errors='coerce')
    total_visits = df['visits'].sum()
    
    df['num_articles'] = np.floor(num_articles * (df['visits'] / total_visits))
    assigned = int(df['num_articles'].sum())
    remainder = int(num_articles - assigned)
    fractions = num_articles * (df['visits'] / total_visits) - df['num_articles']
    df.loc[fractions.nlargest(remainder).index, 'num_articles'] += 1
    df['num_articles'] = df['num_articles'].astype(int)

    df.to_csv(os.path.join(SCRIPT_DIR, '..', 'data', 'domains_w_quotas.csv'))

if __name__ == "__main__":
    main()