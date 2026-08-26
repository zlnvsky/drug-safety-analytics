# Project Plan — Drug Safety Analytics Platform

## Sprint 0 — Project Planning

### Goal

Analyze adverse event reports to identify and prioritize high-risk drug safety signals for further investigation.

[//]: # (Define business problem, dataset, architecture and analytics strategy.)

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

[//]: # (Analyze adverse event reports to identify and prioritize high-risk drug safety signals for further investigation.)

[//]: # (Analyze adverse drug events to identify high-risk drugs, patient groups, and safety patterns.&#41; old)


---

## Business Questions

(To be finalized, current draft)

* Which drugs are associated with the highest number of serious adverse events?
* Which patient demographics show higher risk of severe outcomes?
* Are serious adverse event reports increasing over time for specific drugs?
* Which drug-reaction combinations are most frequently associated with serious outcomes?

[//]: # (* How do adverse events vary over time?)
[//]: # (* Which drug-reaction combinations are most critical?)
[//]: # (* Are there patterns indicating increased risk due to drug interactions?)

---

## Primary Business Metric (Draft)

Serious Adverse Event Rate per Drug:

* proportion of serious outcomes (death, hospitalization, life-threatening events)
* grouped by drug and manufacturer

---

## Data Source

FDA FAERS dataset

---

## Next Steps

Sprint 1:

* Download FAERS data
* Understand schema (DEMO, DRUG, REAC, OUTC)
* Build initial data model
* Load into Python environment
