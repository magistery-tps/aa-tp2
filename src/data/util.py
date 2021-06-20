import pandas as pd

def exclude_columns(df, columns): 
    return df.drop(columns, axis=1)