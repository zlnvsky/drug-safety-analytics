import pandas as pd
from src.config import UNKNOWN_VALUES, MAX_UNIQUE_VALUES

def rename_columns(df):
    """
    Rename and standardize column names in a dataframe.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', '_', regex=True)
        .str.replace(r'[^\w]', '', regex=True)
    )
    return df

def normalize_str_values(df):
    """
    Normalize string values: uppercase, strip, remove special characters.
    """
    df = df.copy()
    str_cols = df.select_dtypes(['str', 'object']).columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.upper().str.strip())
    df[str_cols] = df[str_cols].apply(lambda x: x
        .str.replace('.', '', regex=False)
        .str.replace('-', ' ', regex=False)
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True))
    return df


def standardize_unknown(df):
    """
    Replace common unknown/missing string values with UNK.
    """
    df = df.copy()
    str_cols = df.select_dtypes(['str', 'object']).columns
    df[str_cols] = df[str_cols].replace(UNKNOWN_VALUES, 'UNK')
    df[str_cols] = df[str_cols].apply(
        lambda x: x.str.replace(r'.*UNKNOWN.*', 'UNK', regex=True)
    )
    return df


def fill_str_nulls(df):
    """
    Fill string columns NaN values with UNK.
    """
    df = df.copy()
    str_cols = df.select_dtypes(['str', 'object']).columns
    df[str_cols] = df[str_cols].fillna('UNK')
    return df


def convert_str_to_cat(df):
    """
    Convert string columns with fewer than MAX_UNIQUE_CAT values to category dtype.
    """
    df = df.copy()
    str_cols = df.select_dtypes(['str', 'object']).columns
    for col in str_cols:
        if df[col].nunique() <= MAX_UNIQUE_VALUES:
            df[col] = df[col].astype('category')
    return df


def drop_duplicates(df):
    """
    Drop duplicate records.
    """
    df = df.copy()
    return df.drop_duplicates()