import pandas as pd
from src.config import UNKNOWN_VALUES, MAX_UNIQUE_CAT
from src.utils import rename_columns, standardize_unknown, fill_str_nulls, convert_str_to_cat, drop_duplicates

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
    df = df[['primaryid', 'caseid',
             'drug_seq', 'role_cod', 'drugname', 'prod_ai',
             'route', 'dose_form']]
    return df

# ============================================================
# 3. CREATE FEATURES
# ============================================================

# 3.1 Normalize drug name columns
def normalize_drug_names(df):
    """
    Normalize drugname and prod_ai columns.
    """
    df = df.copy()
    cols = ['drugname', 'prod_ai']
    df[cols] = df[cols].apply(lambda x: x
        .str.upper()
        .str.strip()
        .str.replace('.', '', regex=False)
        .str.replace('-', ' ', regex=False)
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True))
    return df

# 3.2 Create is_primary column
def create_is_primary(df):
    """
    Create boolean column indicating primary suspect drug.
    """
    df = df.copy()
    df['is_primary'] = df['role_cod'] == 'PS'
    return df

# 3.3 Final column selection
def select_columns_final(df):
    """
    Final column selection for analysis.
    """
    df = df.copy()
    df = df[['primaryid', 'caseid',
             'drug_seq', 'role_cod', 'drugname', 'prod_ai',
             'route', 'dose_form', 'is_primary', 'drugs_per_case']]
    return df

# ============================================================
# 4. REMOVE DUPLICATES
# ============================================================

def drop_drug_duplicates(df):
    """
    Remove duplicate drug records keeping first occurrence.
    """
    df = df.copy()
    df = df.drop_duplicates(subset=['primaryid', 'prod_ai', 'route'], keep='first')
    return df

# ============================================================
# 5. REMOVE ANOMALIES
# ============================================================

# 5.1 Remove UNK route duplicates
def drop_unk_route_duplicates(df):
    """
    Remove records where route is UNK if a specific route exists
    for the same drug in the same case.
    """
    df = df.copy()
    df_routes = df.groupby(['primaryid', 'prod_ai'], as_index=False).agg(
        routes=('route', list),
        unique_routes=('route', 'nunique')
    )
    mask = (
        (df_routes['unique_routes'] > 1) &
        (df_routes['routes'].apply(lambda x: 'UNK' in x))
    )
    unk_duplicates = df_routes[mask][['primaryid', 'prod_ai']]
    df = df[~(
        df[['primaryid', 'prod_ai']].apply(tuple, axis=1).isin(
            unk_duplicates.apply(tuple, axis=1)
        ) & (df['route'] == 'UNK')
    )]
    return df

# ============================================================
# 6. CONVERT TYPES
# ============================================================

def convert_role_cod(df):
    """
    Convert role_cod to ordered categorical dtype.
    """
    df = df.copy()
    role_order = pd.CategoricalDtype(['C', 'I', 'SS', 'PS'], ordered=True)
    df['role_cod'] = df['role_cod'].astype(role_order)
    return df

# ============================================================
# 7. REORDER & RECALCULATE
# ============================================================

def recalculate_drug_seq(df):
    """
    Sort by primaryid and role_cod, recalculate drug_seq and drugs_per_case.
    """
    df = df.copy()
    df = df.sort_values(['primaryid', 'role_cod'], ascending=[True, False])
    df = df.reset_index(drop=True)
    df['drug_seq'] = df.groupby('primaryid').cumcount() + 1
    df['drugs_per_case'] = df.groupby('primaryid')['drug_seq'].transform('max')
    return df

# ============================================================
# MAIN PIPELINE
# ============================================================

def clean_drug(df):
    """
    Full cleaning pipeline for DRUG table.
    """
    df = rename_columns(df)
    df = select_columns(df)
    df = normalize_drug_names(df)
    df = standardize_unknown(df)
    df = fill_str_nulls(df)
    df = create_is_primary(df)
    df = drop_drug_duplicates(df)
    df = drop_unk_route_duplicates(df)
    df = convert_role_cod(df)
    df = convert_str_to_cat(df)
    df = recalculate_drug_seq(df)
    df = select_columns_final(df)
    df = drop_duplicates(df)
    return df