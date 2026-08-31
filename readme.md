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

## 🧱 Data Source

FDA Adverse Event Reporting System (FAERS)
https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html

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
* ✅ Sprint 3 — Data Cleaning: REAC, OUTC, INDI
* 🔄 Sprint 4 — Analysis & Business Questions
* ⏳ Sprint 5 — Dashboard (Power BI)

---
