
# app.py
import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # safety: ensure expected cols exist
    need = ["npi","specialty_description","nppes_provider_state","total_rx","patient_volume",
            "pct_first_line","pct_innovative","pct_dpp4","pct_legacy","pct_insulin","pct_tzd",
            "care_gap_score","innovation_score","segment"]
    for c in need:
        if c not in df.columns: df[c] = 0.0 if c.startswith("pct_") or c.endswith("score") else ""
    df["care_gap_score"] = df["care_gap_score"].clip(upper=10)
    return df

st.set_page_config(page_title="Care Gap & HCP Segmentation", layout="wide")
st.title("Care Gap & HCP Segmentation (CMS Part D 2023)")

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

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("HCPs", f"{d['npi'].nunique():,}")
k2.metric("Total Rx", f"{int(d['total_rx'].sum()):,}")
k3.metric("Mean Innovation", f"{d['innovation_score'].mean():.2f}")
k4.metric("Mean Care Gap", f"{d['care_gap_score'].mean():.2f}")

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
