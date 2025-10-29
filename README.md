# 🩺 HCP Care Gap & Segmentation

**Author:** Erica Brooks  
**Dataset:** CMS Part D Prescriber PUF (2023)  
**Tech Stack:** Python, Pandas, Plotly, Matplotlib, ReportLab, Streamlit  

---

## 🎯 Project Overview
This project analyzes U.S. prescribing patterns to identify **care gaps** and **innovation adoption** among healthcare providers (HCPs) using the **CMS Part D Prescriber PUF (2023)** dataset.

The goal was to build an end-to-end analytics pipeline that could help a pharmaceutical Medical Affairs team (e.g., Pfizer) segment prescribers into meaningful groups for education, outreach, and strategic planning.

---

## 🧩 Problem Statement
How can we identify and segment prescribers based on **adherence to diabetes treatment guidelines** and **adoption of innovative therapies** (GLP-1, SGLT2, dual agonists), while detecting **care gaps** and **DPP-4 heavy reliance**?

---

## ⚙️ Pipeline Summary
**Data Source:** CMS Part D Prescriber PUF (2023)

**Pipeline Steps**
1. **Data Preparation**
   - Streamed the large CMS dataset in chunks for performance.
   - Normalized drug names and split combination therapies.
   - Mapped all drugs into therapeutic classes:
     - First-line (Metformin)
     - Innovative (GLP-1, SGLT2, Dual Agonists)
     - DPP-4 (separate class)
     - Legacy (Sulfonylureas, Meglitinides, Alpha-glucosidase inhibitors)
     - Insulin, TZD, Other
2. **Feature Engineering**
   - Calculated % share by class for each HCP.
   - Computed **Care Gap Score** and **Innovation Score**.
3. **Segmentation**
   - Defined percentile-based cohorts:
     - **Innovators** (top 10% innovation)
     - **High Gap** (top 10% care gap, low first-line)
     - **DPP-4 Heavy** (top 10% DPP-4 usage)
     - **Guideline-Aligned** (high first-line, low legacy)
4. **Visualization**
   - Scatter: *Care Gap vs Innovation*  
   - Stacked bar: *Therapy Mix by Specialty*  
   - Choropleth: *State-level DPP-4 adoption*
5. **Reporting**
   - Generated a full PDF case study with visuals and recommendations.
   - Built an interactive Streamlit dashboard for dynamic exploration.

---

## 📊 Key Findings
- **Primary Care** (Family Practice, Internal Medicine, NPs) drives volume but shows moderate innovation adoption.  
- **Endocrinology** and **Nephrology** lead in GLP-1/SGLT2 adoption, aligning with guideline leadership.  
- **~7k DPP-4 Heavy prescribers** represent a key opportunity for educational or formulary support.  
- **High-Gap prescribers** cluster in primary care specialties, suggesting targeted outreach potential.

---

## 🖼️ Visuals

| Visualization | Description |
|----------------|-------------|
| ![Scatter](reports/figures/scatter_gap_innov_dpp4.png) | **Figure 1.** Care Gap vs Innovation (size/color = DPP-4 share, color = segment) |
| ![Stacked](reports/figures/shares_by_specialty.png) | **Figure 2.** Therapy Mix by Specialty (includes DPP-4 category) |
| 🗺️ [Interactive DPP-4 Map (GitHub Pages)](https://brookserica.github.io/hcp-care-gap/state_dpp4.html) | **Figure 3.** Mean DPP-4 Share by State (interactive) |

---

## 🧮 Data Quality & Validation
- Verified unique NPI–Specialty–State grain.  
- Ensured totals match (`sum(categories) == total_rx`).  
- Percentages constrained to [0,1].  
- No duplicates or negative values.  
- Extreme care-gap values capped at 10 for interpretability.

---

## 🧰 Repository Structure
hcp-care-gap/
├── data/
│ ├── raw/ # (not uploaded) CMS dataset location
│ ├── out/ # processed output: hcp_caregap_features.csv
├── notebooks/
│ ├── hcp_caregap_partd.ipynb # data prep & mapping
│ ├── hcp_caregap.ipynb # validation checks, plots & charts
├── reports/
│ ├── figures/ # PNGs and HTML map
│ └── case_study_pfizer.pdf
├── src/
│ └── pipeline.py # optional script for pipeline (exported from Colab)
├── app.py # Streamlit dashboard
├── .gitignore
└── README.md


---

📈 Interactive Deliverables

Interactive Map (GitHub Pages):
🔗 https://brookserica.github.io/hcp-care-gap/state_dpp4.html

Streamlit Dashboard: https://hcp-care-gap.streamlit.app/

Full Case Study PDF:
reports/case_study_pfizer.pdf

