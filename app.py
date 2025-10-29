
# app.py
import pandas as pd
import plotly.express as px
import streamlit as st
import base64
from streamlit_pdf_viewer import pdf_viewer
from pathlib import Path

@st.cache_data
def load_data(path_main="data/out/hcp_caregap_features.csv",
              path_sample="data/out/hcp_caregap_features_sample.csv"):
    try:
        df = pd.read_csv(path_main)
    except Exception:
        df = pd.read_csv(path_sample)
    # safety: ensure expected columns exist
    need = ["npi","specialty_description","nppes_provider_state","total_rx","patient_volume",
            "pct_first_line","pct_innovative","pct_dpp4","pct_legacy","pct_insulin","pct_tzd",
            "care_gap_score","innovation_score","segment"]
    for c in need:
        if c not in df.columns:
            df[c] = 0.0 if c.startswith("pct_") or c.endswith("score") else ""
    df["care_gap_score"] = df["care_gap_score"].clip(upper=10)
    return df

st.set_page_config(page_title="HCP Care Gap & Segmentation", layout="wide")
st.title("HCP Care Gap & Segmentation (CMS Part D 2023)")
st.caption("Built by Erica Brooks • PDF case study, GitHub & interactive map links below")

st.markdown(
    """
    **Links:**  
    - 💻 [GitHub repo](https://github.com/BrooksErica/hcp-care-gap)  
    - 🗺️ [Interactive DPP-4 map](https://brookserica.github.io/hcp-care-gap/state_dpp4.html)
    """,
    unsafe_allow_html=True
)

data_path = st.text_input("Path to processed CSV", "data/out/hcp_caregap_sample.csv")
df = load_data(data_path)

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    states = st.multiselect("States", sorted(df["nppes_provider_state"].dropna().unique().tolist()))
with col2:
    specs = st.multiselect("Specialties", sorted(df["specialty_description"].dropna().unique().tolist()))
with col3:
    segs = st.multiselect("Segments", sorted(df["segment"].dropna().unique().tolist()))

mask = pd.Series(True, index=df.index)
if states: mask &= df["nppes_provider_state"].isin(states)
if specs:  mask &= df["specialty_description"].isin(specs)
if segs:   mask &= df["segment"].isin(segs)
d = df[mask].copy()

filtered = d

if d.empty:
    st.warning("No rows match the selected filters. Try broadening your selection.")
    st.stop()

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("HCPs", f"{filtered['npi'].nunique():,}")
k2.metric("Total Rx", f"{int(filtered['total_rx'].sum()):,}")
k3.metric("Mean Innovation", f"{filtered['innovation_score'].mean():.2f}")
k4.metric("Mean Care Gap", f"{filtered['care_gap_score'].mean():.2f}")
st.caption("Care Gap = (legacy+insulin)/first-line. Innovation = GLP-1/SGLT2/dual share. Scores capped for readability.")

st.download_button(
    "Download filtered CSV",
    data=d.to_csv(index=False).encode("utf-8"),
    file_name="hcp_filtered.csv",
    mime="text/csv"
)

# Scatter
st.subheader("Care Gap vs Innovation (color = segment, size = DPP-4 share)")
sample = d.sample(min(len(d), 30000), random_state=42)  # keep it snappy
fig = px.scatter(
    sample, x="care_gap_score", y="innovation_score",
    color="segment", size="pct_dpp4", size_max=18, opacity=0.5,
    hover_data=["npi","specialty_description","nppes_provider_state","total_rx"]
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Specialty table
st.subheader("Specialty Profile (top by volume)")
prof = (d.groupby("specialty_description", as_index=False)
          .agg(hcp_n=("npi","nunique"),
               rx_total=("total_rx","sum"),
               first=("pct_first_line","mean"),
               innov=("pct_innovative","mean"),
               dpp4=("pct_dpp4","mean"),
               legacy=("pct_legacy","mean"),
               gap=("care_gap_score","mean"))
          .sort_values("rx_total", ascending=False)
          .head(20))
st.dataframe(prof)

st.subheader("📄 Case Study PDF")

PDF_PATH = Path("reports/case_study.pdf")
if PDF_PATH.exists():
        pdf_viewer(PDF_PATH.read_bytes(), width=1000)  # renders with pdf.js, no iframe/CORS issues
        st.download_button(
            "Download Case Study PDF",
            data=PDF_PATH.read_bytes(),
            file_name="case_study.pdf",
            mime="application/pdf",
        )
else:
        st.warning("PDF not found at reports/case_study.pdf.")