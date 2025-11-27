import argparse
import os.path
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str, help="Path to 500 article to pick from")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    df_sample = df.sample(n=200)
    df_sample.to_csv(os.path.join(os.path.dirname(__file__), "..", "data", "open_coding_articles.tsv"), sep="\t")

if __name__ == "__main__":
    main()