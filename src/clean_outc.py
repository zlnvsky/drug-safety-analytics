import pandas as pd
from src.utils import rename_columns, normalize_str_values, standardize_unknown, fill_str_nulls, drop_duplicates
from src.config import OUTC_ORDER, OUT_LABELS, OUTCOME_ORDER

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
# 3. CREATE FEATURES
# ============================================================

def create_outcome_col(df):
    """
    Create full-name outcome column.
    """
    df = df.copy()
    df['outcome'] = df['outc_cod'].map(OUT_LABELS)
    return df

# ============================================================
# 4. CONVERT TYPES
# ============================================================

def convert_outc_cod(df):
    """
    Convert outc_cod column to ordered categorical dtype.
    """
    df = df.copy()
    outc_cats = pd.CategoricalDtype(OUTC_ORDER, ordered=True)
    df['outc_cod'] = df['outc_cod'].astype(outc_cats)
    return df


def convert_outcome(df):
    """
    Convert outcome column to ordered categorical dtype.
    """
    df = df.copy()
    outcome_cat = pd.CategoricalDtype(OUTCOME_ORDER, ordered=True)
    df['outcome'] = df['outcome'].astype(outcome_cat)
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
    df = create_outcome_col(df)
    df = normalize_str_values(df)
    df = standardize_unknown(df)
    df = fill_str_nulls(df)
    df = convert_outc_cod(df)
    df = convert_outcome(df)
    df = drop_duplicates(df)
    return df