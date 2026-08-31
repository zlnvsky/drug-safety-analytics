import pandas as pd
from src.utils import rename_columns, normalize_str_values, standardize_unknown, fill_str_nulls, drop_duplicates
from src.config import OUTC_ORDER

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
    df = df[['primaryid', 'caseid', 'outc_cod']]
    return df

# ============================================================
# 3. CONVERT TYPES
# ============================================================

def convert_outc_cod(df):
    """
    Convert outc_cod to ordered categorical dtype.
    """
    df = df.copy()
    outc_cats = pd.CategoricalDtype(OUTC_ORDER, ordered=True)
    df['outc_cod'] = df['outc_cod'].astype(outc_cats)
    return df

# ============================================================
# MAIN PIPELINE
# ============================================================

def clean_outc(df):
    """
    Full cleaning pipeline for OUTC table.
    """
    df = rename_columns(df)
    df = select_columns(df)
    df = normalize_str_values(df)
    df = standardize_unknown(df)
    df = fill_str_nulls(df)
    df = convert_outc_cod(df)
    df = drop_duplicates(df)
    return df