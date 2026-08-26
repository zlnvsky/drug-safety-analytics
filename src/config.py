import pycountry

DATE_FORMAT = "%Y%m%d"

AGE_MULTIPLIERS_DAYS = {
    "DEC": 3652.5,
    "YR": 365,
    "MON": 30,
    "WK": 7,
    "DY": 1,
    "HR": 1 / 24,
}

AGE_MULTIPLIERS_YEARS = {
    'YR': 1,
    'MON': 1/12,
    'WK': 1/52,
    'DY': 1/365,
    'DEC': 10,
    'HR': 1/8760
}

AGE_GROUP_BINS = [0, 28, 730, 4383, 6575, 23725, float('inf')]
AGE_GROUP_LABELS = [
    'Neonate',
    'Infant',
    'Child',
    'Adolescent',
    'Adult',
    'Elderly'
]

WEIGHT_MULTIPLIERS = {
    "KG": 1,
    "LBS": 0.453592,
    "GMS": 0.001,
}

VALID_COUNTRIES = {country.alpha_2 for country in pycountry.countries}

MAX_AGE_DAYS = 365 * 120
MAX_WEIGHT_KG = 301
MIN_WEIGHT_KG = 1

UNKNOWN_VALUES = ['UNKNOWN', 'UNKNWON', 'NOT SPECIFIED', 'NOT REPORTED',
                  'N/A', 'NA', 'NONE', 'NR', '-', '', ' ']

MAX_UNIQUE_CAT = 200