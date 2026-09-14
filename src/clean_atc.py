import pandas as pd
from src.utils import rename_columns, normalize_str_values, fill_str_nulls, drop_duplicates

# ============================================================
# 1. RENAME COLUMNS — see utils.py
# ============================================================

# ============================================================
# 2. SELECT & CLEAN
# ============================================================

def select_columns(df):
    """
    Select relevant ATC columns and drop rows without atc5_description.
    """
    df = df.copy()
    df = df.dropna(subset=['atc5_description'])
    df = df[['atc1_description', 'atc2_description', 'atc3_description',
              'atc4_description', 'atc5_code', 'atc5_description']]
    return df

# ============================================================
# MAIN PIPELINE
# ============================================================

def clean_atc(df):
    """
    Full cleaning pipeline for ATC classification table.
    """
    df = rename_columns(df)
    df = select_columns(df)
    df = normalize_str_values(df)
    df = fill_str_nulls(df)
    df = drop_duplicates(df)
    return df