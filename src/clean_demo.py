import pandas as pd

from src.config import (
    AGE_MULTIPLIERS_DAYS,
    AGE_MULTIPLIERS_YEARS,
    DATE_FORMAT,
    AGE_GROUP_BINS,
    AGE_GROUP_LABELS,
    WEIGHT_MULTIPLIERS,
    MAX_AGE_DAYS,
    MIN_WEIGHT_KG,
    MAX_WEIGHT_KG,
    VALID_COUNTRIES)

from src.utils import (
    rename_columns,
    standardize_unknown,
    fill_str_nulls,
    convert_str_to_cat,
    drop_duplicates)

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
    df = df[['primaryid', 'caseversion',
        'mfr_dt', 'init_fda_dt', 'fda_dt', 'rept_dt', 'rept_cod',
        'age', 'age_grp', 'age_cod', 'sex', 'wt', 'wt_cod',
        'reporter_country', 'occr_country']]
    return df

# ============================================================
# 3. CONVERT DATES
# ============================================================

def convert_faers_dates(df):
    """
    Convert FAERS date columns to datetime.
    """
    df = df.copy()
    dt_list = df.columns[df.columns.str.contains('dt')].tolist()
    for col in dt_list:
        df[col] = pd.to_datetime(
            df[col].astype('Int64').astype(str),
            format=DATE_FORMAT,
            errors='coerce',
        )
    return df

# ============================================================
# 4. CREATE FEATURES
# ============================================================

# 4.1 Create age_days and age_years columns
def create_age_columns(df):
    """
    Create age_days and age_years columns from raw age and age_cod.
    """
    df = df.copy()
    df['age'] = df['age'].astype('Int64')
    df['age_days'] = df['age'] * df['age_cod'].map(AGE_MULTIPLIERS_DAYS)
    df['age_years'] = df['age'] * df['age_cod'].map(AGE_MULTIPLIERS_YEARS)
    return df

# 4.2 Create age_group column
def age_groups(df):
    """
    Create age_group based on age_days column.
    """
    df = df.copy()
    df['age_grp'] = pd.cut(
        df['age_days'],
        bins=AGE_GROUP_BINS,
        labels=AGE_GROUP_LABELS,
        right=False,
        ordered=False
    )
    df['age_grp'] = df['age_grp'].cat.add_categories('UNK')
    df['age_grp'] = df['age_grp'].fillna('UNK')
    return df

# 4.3 Standardize weight column to kg
def weight_kg(df):
    """
    Transform and standardize weight column to kilograms by wt_cod column.
    """
    df = df.copy()
    df['wt_kg'] = df['wt'] * df['wt_cod'].map(WEIGHT_MULTIPLIERS)
    return df

# 4.4 Final column selection
def select_columns_final(df):
    """
    Final column selection for analysis.
    """
    df = df.copy()
    df = df[['primaryid', 'caseversion',
        'rept_cod', 'mfr_dt', 'rept_dt', 'init_fda_dt', 'fda_dt',
        'age_days', 'age_years', 'age_grp', 'sex', 'wt_kg',
        'reporter_country', 'occr_country']]
    return df

# ============================================================
# 5. REMOVE ANOMALIES
# ============================================================

# 5.1.1 Remove anomalies from mfr_dt column
def drop_mfr_anomaly(df):
    """
    Remove records where manufacturer date is later than FDA received date
    excluding direct reports (DIR) as they don't involve manufacturers.
    """
    df = df.copy()
    mfr_anomaly_mask = (df['mfr_dt'] > df['fda_dt']) & (df['rept_cod'] != 'DIR')
    return df[~mfr_anomaly_mask]

# 5.1.2 Remove anomalies from date sequence
def drop_date_anomalies(df):
    """
    Find and remove records where date sequence is violated.
    Expected order: mfr_dt <= rept_dt <= init_fda_dt <= fda_dt.
    """
    df = df.copy()
    dt_cols = df.columns[df.columns.str.contains('dt')].tolist()
    anomaly_mask = pd.Series(False, index=df.index)
    for i in range(len(dt_cols) - 1):
        current = dt_cols[i]
        next_col = dt_cols[i + 1]
        if current == 'rept_dt' and next_col == 'init_fda_dt':
            continue
        anomaly_mask |= df[current] > df[next_col]
    return df[~anomaly_mask]

# 5.2 Remove age anomalies
def remove_invalid_age(df):
    """
    Remove records with implausible age > 120.
    """
    df = df.copy()
    return df[df['age_days'].isna() | (df['age_days'] <= MAX_AGE_DAYS)]

# 5.3 Remove weight anomalies
def remove_invalid_weight(df):
    """
    Remove records with implausible weight > 300 and < 1 kg.
    """
    df = df.copy()
    return df[df['wt_kg'].isna() | (df['wt_kg'] < MAX_WEIGHT_KG) & (df['wt_kg'] > MIN_WEIGHT_KG)]

# 5.4 Remove country anomalies
def clean_invalid_countries(df):
    """
    Identify country columns and replace incorrect values with UNK.
    """
    df = df.copy()
    country_cols = df.columns[df.columns.str.contains('country')]
    for col in country_cols:
        anomaly_countries = (
            df[(df[col].isna()) | (~df[col].isin(VALID_COUNTRIES))][col]
            .value_counts()
            .index
            .tolist()
        )
        country_mask = {i: 'UNK' for i in anomaly_countries}
        df[col] = df[col].replace(country_mask)
    return df

# ============================================================
# 6. HANDLE NULLS — see utils.py
# ============================================================

# ============================================================
# 7. CONVERT TYPES — see utils.py
# ============================================================

# ============================================================
# 8. REMOVE DUPLICATES — see utils.py
# ============================================================

# ============================================================
# MAIN PIPELINE
# ============================================================

def clean_demo(df):
    df = rename_columns(df)
    df = select_columns(df)
    df = standardize_unknown(df)
    df = fill_str_nulls(df)
    df = convert_faers_dates(df)
    df = create_age_columns(df)
    df = age_groups(df)
    df = weight_kg(df)
    df = select_columns_final(df)
    df = drop_mfr_anomaly(df)
    df = drop_date_anomalies(df)
    df = remove_invalid_age(df)
    df = remove_invalid_weight(df)
    df = clean_invalid_countries(df)
    df = convert_str_to_cat(df)
    df = drop_duplicates(df)
    return df