"""
Map drugs to ATC classes using multiple sources:
1. RxNav API results cached by prod_ai
2. RxNav API results cached by drugname
3. DrugCentral INN names
4. Salt-suffix stripping as a fallback for near-misses

Run the RxNav fetch scripts first (map_drugs_to_atc) before using
this module — it reads from the cache files they produce.
"""

import json
import pandas as pd

from src.utils import normalize_str_values, strip_salt_suffix


def load_rxnav_cache(path):
    """
    Load a RxNav API cache file (drug name -> ATC class or None).
    """
    with open(path, 'r') as f:
        return json.load(f)


def load_drugcentral_inn(path):
    """
    Load DrugCentral structures.smiles.tsv and return a set of
    normalized INN names.
    """
    df = pd.read_csv(
        path, sep='\t',
        names=['smiles', 'inchi', 'inchikey', 'id', 'inn', 'cas_rn']
    )
    inn_set = set(df['inn'].dropna().str.upper().str.strip())
    return inn_set


def build_atc_lookup(cache_prod_ai_path, cache_drugname_path, drugcentral_path):
    """
    Combine all three sources into a single lookup dict mapping a
    (possibly salt-stripped) drug name to True if an ATC/INN match
    exists in any source. Also returns the raw prod_ai / drugname
    ATC class caches for direct annotation.
    """
    cache_prod_ai = load_rxnav_cache(cache_prod_ai_path)
    cache_drugname = load_rxnav_cache(cache_drugname_path)
    inn_set = load_drugcentral_inn(drugcentral_path)

    known_names = set(cache_prod_ai.keys()) | set(cache_drugname.keys()) | inn_set

    return {
        'cache_prod_ai': cache_prod_ai,
        'cache_drugname': cache_drugname,
        'inn_set': inn_set,
        'known_names': known_names,
    }


def annotate_atc(df, name_col, cache_prod_ai_path, cache_drugname_path, drugcentral_path):
    """
    Add ATC annotation columns to df based on name_col (e.g. 'prod_ai').

    Adds:
    - atc_by_ai / atc_by_name: ATC class string from RxNav, where available
    - atc_final: atc_by_ai, falling back to atc_by_name, filled with 'UNK'
      where neither source matched
    - atc_final_norm: atc_final normalized the same way WHO ATC
      descriptions are normalized in clean_atc.py (uppercase, no dots/
      hyphens, collapsed whitespace), so it can be joined against
      clean_atc.py output (e.g. on atc4_description) to recover a
      broader ATC level such as atc2_description
    - atc_matched: True if the (salt-stripped) name is found in any
      of the three sources, even when no ATC class string was returned
    """
    lookup = build_atc_lookup(cache_prod_ai_path, cache_drugname_path, drugcentral_path)

    df = df.copy()

    df_by_ai = pd.DataFrame(
        list(lookup['cache_prod_ai'].items()), columns=['prod_ai', 'atc_by_ai']
    )
    df_by_name = pd.DataFrame(
        list(lookup['cache_drugname'].items()), columns=['drugname', 'atc_by_name']
    )

    df = df.merge(df_by_ai, on='prod_ai', how='left')
    df = df.merge(df_by_name, on='drugname', how='left')
    df['atc_final'] = df['atc_by_ai'].fillna(df['atc_by_name'])

    str_cols = df.select_dtypes('str').columns.tolist()
    df[str_cols] = df[str_cols].fillna('UNK')

    stripped = df[name_col].apply(strip_salt_suffix)
    df['atc_matched'] = stripped.isin(lookup['known_names']) | df[name_col].isin(lookup['known_names'])

    # Normalize atc_final the same way WHO ATC descriptions are
    # normalized in clean_atc.py, so the two can be joined on a
    # common broader ATC level (e.g. atc4_description).
    tmp = df[['atc_final']].rename(columns={'atc_final': 'atc_final_norm'})
    tmp = normalize_str_values(tmp)
    df['atc_final_norm'] = tmp['atc_final_norm']

    return df


if __name__ == '__main__':
    # Example usage:
    # df_drug = pd.read_csv('data/clean/drug_clean.csv')
    # df_drug = annotate_atc(
    #     df_drug,
    #     name_col='prod_ai',
    #     cache_prod_ai_path='data/atc/rxnav_atc_cache.json',
    #     cache_drugname_path='data/atc/rxnav_atc_cache_drugname.json',
    #     drugcentral_path='data/atc/drugcentral_inn.tsv',
    # )
    #
    # from src.clean_atc import clean_atc
    # df_atc = pd.read_csv('data/atc/who_atc_ddd_2026_2026-02-23.csv')
    # df_atc = clean_atc(df_atc)
    #
    # df_drug = df_drug.merge(
    #     df_atc[['atc4_description', 'atc2_description']].drop_duplicates(),
    #     left_on='atc_final_norm',
    #     right_on='atc4_description',
    #     how='left'
    # )
    pass