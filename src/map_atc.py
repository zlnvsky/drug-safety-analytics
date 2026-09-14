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

SALT_SUFFIXES = [
    ' HYDROCHLORIDE', ' SODIUM', ' SULFATE', ' ACETATE', ' MALEATE',
    ' TARTRATE', ' CITRATE', ' PHOSPHATE', ' MESYLATE', ' FUMARATE',
    ' CALCIUM', ' POTASSIUM', ' DIHYDROCHLORIDE', ' BESYLATE',
    ' HYDROBROMIDE', ' SUCCINATE', ' HEMIHYDRATE', ' MONOHYDRATE',
    ' DIHYDRATE', ' ANHYDROUS', ' TRIHYDRATE'
]


def strip_salt_suffix(name):
    """
    Remove a trailing salt/hydrate suffix from a drug name, if present.
    """
    for suffix in SALT_SUFFIXES:
        if name.endswith(suffix):
            return name[:-len(suffix)].strip()
    return name


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
    Add ATC annotation columns to df based on name_col (e.g. 'prod_ai'):
    - atc_by_ai / atc_by_name: ATC class string from RxNav, where available
    - atc_final: atc_by_ai, falling back to atc_by_name
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

    stripped = df[name_col].apply(strip_salt_suffix)
    df['atc_matched'] = stripped.isin(lookup['known_names']) | df[name_col].isin(lookup['known_names'])

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
    # print(df_drug['atc_matched'].mean())
    pass