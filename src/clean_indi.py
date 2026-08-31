import pandas as pd
from src.utils import rename_columns, normalize_str_values, standardize_unknown, fill_str_nulls, convert_str_to_cat, drop_duplicates

# ============================================================
# 1. RENAME COLUMNS — see utils.py
# ============================================================

# ============================================================
# 2. INITIAL COLUMN SELECTION
# ============================================================

def select_columns(df):
    """
    Select relevant columns for analysis.
    """
    df = df.copy()
    df = df[['primaryid', 'caseid', 'indi_drug_seq', 'indi_pt']]
    return df

# ============================================================
# MAIN PIPELINE
# ============================================================

def clean_indi(df):
    """
    Full cleaning pipeline for INDI table.
    """
    df = rename_columns(df)
    df = select_columns(df)
    df = normalize_str_values(df)
    df = standardize_unknown(df)
    df = fill_str_nulls(df)
    df = convert_str_to_cat(df)
    df = drop_duplicates(df)
    return df