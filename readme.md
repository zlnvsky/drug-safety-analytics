# Drug Safety Analytics Platform

## 🧠 Project Overview

This project simulates a real-world pharmacovigilance analytics system built on FDA FAERS adverse event data.

The goal is to analyze drug safety signals, identify high-risk medications, and support decision-making in 
pharmaceutical safety monitoring.

---

## 🎯 Business Problem

Pharmaceutical companies receive a large volume of adverse event reports every quarter. Manual analysis of these 
reports is slow and may delay the detection of critical safety issues.

This project aims to build an end-to-end analytics pipeline that helps prioritize and analyze adverse drug 
events efficiently.

---

## 📊 Key Objectives

* Analyze adverse event patterns across drugs and patients
* Identify high-risk medications and outcomes
* Explore demographic and temporal factors
* Build a structured data pipeline for analysis
* Provide insights for pharmacovigilance decision-making

---

## 💡 Business Questions

* Which drugs are associated with the highest number of serious adverse events?
* Which drugs are most frequently linked to death outcomes?
* Which drug combinations are the most dangerous?
* Which adverse reactions are most common for specific drug classes?
* Are there age or gender groups at higher risk of serious outcomes?
* Which routes of administration or dose forms are associated with the highest number of adverse events?

---

## 🔬 Advanced Analysis: Disproportionality Signal Detection

In addition to simple frequency counts, this project applies the 
Proportional Reporting Ratio (PRR) — a standard pharmacovigilance 
signal detection method used by regulators (FDA, EMA) — to identify 
adverse reactions that occur disproportionately often for a specific 
drug class, rather than reactions that are simply common overall.

**Method**: For each (drug class, reaction) pair, PRR compares the 
proportion of cases with that reaction within the class against the 
proportion of cases with that reaction among all other classes. 
A continuity correction (+0.5) is applied to avoid division by zero 
when a reaction is unique to one class.

**Output**: A separate table (drug_class, reaction, n_cases, 
total_cases, PRR) intended for export to the BI dashboard, where 
a minimum class-size filter can be applied interactively to balance 
signal strength against statistical reliability.

---

## 🧱 Data Source

FDA Adverse Event Reporting System (FAERS)
https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html

---

## 📥 Data Setup

1. Download FAERS quarterly data from the link above
2. Extract the ASCII files
3. Place them in the `data/` folder:

```
data/
├── DEMO24Q2.txt
├── DRUG24Q2.txt
├── REAC24Q2.txt
├── OUTC24Q2.txt
└── INDI24Q2.txt
```

---

## 🛠️ Tech Stack

* Python (pandas, numpy)
* SQL (PostgreSQL)
* PyCharm
* Git / GitHub
* Power BI (dashboarding)
* Claude (AI pair programming assistant)

---

## 📁 Project Structure

```
drug-safety-analytics/
├── src/
│   ├── clean_demo.py
│   ├── clean_drug.py
│   ├── clean_reac.py
│   ├── clean_outc.py
│   ├── clean_indi.py
│   ├── utils.py
│   └── config.py
├── notebooks/
├── data/
├── sql/
├── dashboard/
├── README.md
├── PROJECT_PLAN.md
└── requirements.txt
```
---

## 🚧 Status

* ✅ Sprint 0 — Project Planning
* ✅ Sprint 1 — Data Cleaning: DEMO
* ✅ Sprint 2 — Data Cleaning: DRUG
* ✅ Sprint 3 — Data Cleaning: REAC, OUTC, INDI, ATC
* 🔄 Sprint 4 — Analysis & Business Questions
* ⏳ Sprint 5 — Dashboard (Power BI)

---

## ⚠️ Known Limitations

**ATC classification coverage**: Drug-to-ATC-class mapping achieves ~99.95% coverage
using RxNav API (by prod_ai and drugname) combined with DrugCentral INN names and
salt-suffix normalization. The WHO ATC/DDD index (see `clean_atc.py`) was evaluated
as an additional source but added negligible coverage (7 of 674 remaining unmatched
entries) and was not included in the final pipeline.

**Causality vs correlation for death outcomes**: FAERS captures temporal 
association between drug use and adverse events, not confirmed causality. 
This is especially relevant for oncology drugs (e.g. TAGRISSO, VENCLEXTA, 
TECENTRIQ) where death may reflect disease progression rather than drug 
toxicity, since these drugs treat severe, often terminal conditions.

**Salt suffix normalization**: A curated list of common salt/hydrate suffixes 
(e.g. HYDROCHLORIDE, SODIUM, MESYLATE) is stripped from prod_ai to consolidate 
different salt forms of the same active ingredient (e.g. LENVATINIB vs 
LENVATINIB MESYLATE) under prod_ai_clean. This list is not exhaustive — rarer 
salt forms not covered by the list remain as distinct entries, slightly 
understating consolidation but not introducing false matches.

**drug_seq recalculated**: The DRUG table's drug_seq is recalculated after 
deduplication to number Primary Suspect (PS) drugs first within each case, 
so it no longer matches the original FAERS drug_seq used to join against 
the THER (therapy dates) file. The original sequence is preserved separately 
if a THER join is needed in future work.