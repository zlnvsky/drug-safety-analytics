# Project Plan — Drug Safety Analytics Platform

## ✅ Sprint 0 — Project Planning

### Goal
Define business problem, dataset, architecture and analytics strategy.

---

## Business Problem

Pharmaceutical companies receive thousands of adverse event reports
from healthcare professionals, patients, and manufacturers.
Due to the large volume of reports, it is difficult to identify which safety signals
require immediate investigation and which patient groups are at the highest risk.

The objective of this project is to analyze adverse event reports,
identify high-risk drugs, patient groups, and safety patterns,
and provide data-driven insights to support pharmacovigilance decision-making
and safety monitoring.

---

## Business Questions

* Which drugs are associated with the highest number of serious adverse events?
* Which drugs are most frequently linked to death outcomes?
* Which drug combinations are the most dangerous?
* Which adverse reactions are most common for specific drug classes?
* Are there age or gender groups at higher risk of serious outcomes?
* Which routes of administration or dose forms are associated with the highest number of adverse events?

---

## Primary Business Metric

Serious Adverse Event Rate per Drug:

* Proportion of serious outcomes (death, hospitalization, life-threatening events)
* Grouped by drug and manufacturer

---

## Data Source

FDA Adverse Event Reporting System (FAERS)
https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html

---

## ✅ Sprint 1 — Data Cleaning: DEMO

### Goal
Clean and standardize the DEMO table for analysis.

### Completed
* Standardized column names
* Selected relevant columns
* Converted date columns to datetime format
* Created age_days, age_years, age_grp features
* Standardized weight to kg
* Removed date anomalies
* Removed age and weight outliers
* Standardized country columns
* Handled missing values
* Converted categorical columns

---

## ✅ Sprint 2 — Data Cleaning: DRUG

### Goal
Clean and standardize the DRUG table for analysis.

### Completed
* Standardized column names
* Selected relevant columns
* Normalized drugname and prod_ai columns
* Removed duplicates
* Removed UNK route duplicates
* Created is_primary feature
* Recalculated drug_seq and drugs_per_case
* Converted categorical columns

---

## ✅ Sprint 3 — Data Cleaning: REAC, OUTC, INDI, ATC

### Goal
Clean and standardize REAC, OUTC, INDI and ATC reference tables for analysis.

### Completed
* Cleaned REAC table (reactions, drug_rec_act)
* Cleaned OUTC table (outcomes with ordered categorical)
* Cleaned INDI table (drug indications)
* Cleaned ATC classification reference table (WHO)
* Added normalize_str_values() to shared utils
* Added OUTC_ORDER constant to config

---

## 🔄 Sprint 4 — Analysis & Business Questions

### Goal
Answer 6 business questions using cleaned data.

### Completed
* Q1: Top drugs and ATC classes by serious adverse events (solo and multi-drug cases)
* Q2: Top drugs and ATC classes by death outcomes (solo and multi-drug cases)
* Q3: Most frequent multi-drug combinations (salt-normalized via prod_ai_clean)
* Q4: Top reactions per ATC class (simple frequency)
* Implemented PRR-based signal detection for drug class → reaction analysis
### Next Steps
* Q5: Age/gender risk groups for serious outcomes
* Q6: Route/dose form vs adverse event frequency

---

## ⏳ Sprint 5 — Dashboard (Power BI)

### Goal
Build interactive dashboard for pharmacovigilance insights.