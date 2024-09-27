import pandas as pd
import os


def produce_evals(location):
    df = pd.read_csv(location)
    return df['value'].mean(), df.groupby('index')['value'].mean().mean(), df['index'].unique().shape[0]/50, df['value'].sum()


if __name__ == '__main__':
    for location in os.listdir('./evals/'):
        print(location, produce_evals('./evals/' + location))
