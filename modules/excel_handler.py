import pandas as pd

def read_excel(path):
    return pd.read_excel(path, engine='openpyxl')


def write_excel(df, path):
    df.to_excel(path, index=False)
