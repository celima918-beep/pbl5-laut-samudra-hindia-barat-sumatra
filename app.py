import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Estimasi Stok Ikan Sumatra", layout="wide")

st.title("🐟 Estimasi Stok Ikan Berbasis Data Satelit")
st.write("Simulasi integrasi data oseanografi Suhu dan Klorofil untuk memprediksi fluktuasi biomassa perairan barat Sumatra.")

# Membuat data riil Sumatra milik Anda langsung di dalam kode program
data_riil = {
    "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"],
    "Suhu_Laut_C": [29.09, 29.02, 29.39, 29.74, 30.02, 30.07, 29.88, 29.61, 29.41, 29.75, 29.44, 29.24],
    "Klorofil_a": [0.21651414, 0.19403403, 0.17957865, 0.16867486, 0.1776436, 0.17800032, 0.18564603, 0.20808287, 0.1887339, 0.17397971, 0.27566928, 0.25348687],
    "Luas_Habitat": [475248, 475248, 475248, 475248, 475248, 475248, 475248, 475248, 475248, 475248, 475248, 475248]
}
df = pd.DataFrame(data_riil)

# Membuat panel input parameter model estimasi di sebelah kiri
st.sidebar.header("Parameter Model Estimasi")
st.sidebar.write("Sesuaikan sensitivitas ikan terhadap lingkungan:")

suhu_optimal = st.sidebar.slider("Suhu Optimal Ikan (°C)", 25.00, 35.00, 28.50, 0.10)
alfa_klorofil = st.sidebar.slider("Faktor Pengali Klorofil (α)", 500, 5000, 3000, 100)
beta_penalti_suhu = st.sidebar.slider("Faktor Penalti Suhu (β)", 100, 1000, 500, 50)

# Menghitung rumus estimasi stok ikan secara otomatis menggunakan parameter slider
df["Penalti_Suhu"] = (df["Suhu_Laut_C"] - suhu_optimal).abs() * beta_penalti_suhu
df["Estimasi_Stok"] = (df["Luas_Habitat"] * 1.5) + (df["Klorofil_a"] * alfa_klorofil) - df["Penalti_Suhu"]
df["Estimasi_Stok"] = df["Estimasi_Stok"].round(0).astype(int)

# Membuat tampilan visualisasi grafik atas
col1, col2 = st.columns(2)

with col1:
    st.write("### Tren Suhu dan Klorofil Bulanan")
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(x=df["Bulan"], y=df["Suhu_Laut_C"], name="Suhu (°C)", mode="lines+markers", line=dict(color="crimson")), secondary_y=False)
    fig1.add_trace(go.Scatter(x=df["Bulan"], y=df["Klorofil_a"], name="Klorofil (mg/m³)", mode="lines+markers", line=dict(color="green", dash="dash")), secondary_y=True)
    fig1.update_layout(xaxis_title="Bulan", yaxis_title="Suhu Laut (°C)", yaxis2_title="Klorofil_a (mg/m³)", legend=dict(x=1.1, y=1.1))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.write("### Fluktuasi Estimasi Stok Ikan (Biomassa)")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df["Bulan"], y=df["Estimasi_Stok"], name="Estimasi Stok", marker_color="cadetblue"))
    fig2.add_trace(go.Scatter(x=df["Bulan"], y=df["Estimasi_Stok"], mode="lines+markers", line=dict(color="orange"), name="Tren"))
    fig2.update_layout(xaxis_title="Bulan", yaxis_title="Estimasi Stok")
    st.plotly_chart(fig2, use_container_width=True)

# Tampilan tabel detail data mentah di bagian bawah
st.write("### Lihat Detail Data Mentah")
st.dataframe(df[["Bulan", "Suhu_Laut_C", "Klorofil_a", "Estimasi_Stok"]], use_container_width=True)
