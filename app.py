import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Estimasi Stok Ikan Sumatra - Kelompok 9", layout="wide")

# Menampilkan identitas anggota kelompok 9 pada bagian paling atas aplikasi
st.subheader("Kelompok 9")
st.text("1. Ina Rani Amelia (10090224002)\n2. Nayla Dwi Safitri (10090224007)\n3. Celi Maulidi Aprilia (10090224027)")

st.title("🐟 Estimasi Stok Ikan Berbasis Data Satelit")
st.write("Simulasi integrasi data oseanografi Suhu dan Klorofil untuk memprediksi fluktuasi biomassa perairan barat Sumatra.")

# Memasukkan data riil 4 kolom milik Anda langsung ke dalam struktur data program
data_sumatra = {
    "Bulan": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Nama_Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"],
    "Suhu_Laut_C": [29.09, 29.02, 29.39, 29.74, 30.02, 30.07, 29.88, 29.61, 29.41, 29.75, 29.44, 29.24],
    "Klorofil": [0.21651414, 0.19403403, 0.17957865, 0.16867486, 0.1776436, 0.17800032, 0.18564603, 0.20808287, 0.1887339, 0.17397971, 0.27566928, 0.25348687]
}
df = pd.DataFrame(data_sumatra)

# Membuat panel input parameter model estimasi di sebelah kiri
st.sidebar.header("Parameter Model Estimasi")
st.sidebar.write("Sesuaikan sensitivitas ikan terhadap lingkungan:")

suhu_optimal = st.sidebar.slider("Suhu Optimal Ikan (°C)", 25.00, 35.00, 28.50, 0.10)
alfa_klorofil = st.sidebar.slider("Faktor Pengali Klorofil (α)", 500, 5000, 3000, 100)
beta_penalti_suhu = st.sidebar.slider("Faktor Penalti Suhu (β)", 100, 1000, 500, 50)

# Menghitung rumus estimasi stok ikan secara otomatis menggunakan konstanta luas 1000
luas_konstan = 1000
df["Penalti_Suhu"] = (df["Suhu_Laut_C"] - suhu_optimal).abs() * beta_penalti_suhu
df["Estimasi_Stok"] = (luas_konstan * 1.5) + (df["Klorofil"] * alfa_klorofil) - df["Penalti_Suhu"]
df["Estimasi_Stok"] = df["Estimasi_Stok"].round(0).astype(int)

# Membuat tampilan visualisasi grafik atas
col1, col2 = st.columns(2)

with col1:
    st.write("### Tren Suhu dan Klorofil Bulanan")
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(x=df["Nama_Bulan"], y=df["Suhu_Laut_C"], name="Suhu (°C)", mode="lines+markers", line=dict(color="crimson")), secondary_y=False)
    fig1.add_trace(go.Scatter(x=df["Nama_Bulan"], y=df["Klorofil"], name="Klorofil (mg/m³)", mode="lines+markers", line=dict(color="green", dash="dash")), secondary_y=True)
    fig1.update_layout(xaxis_title="Bulan", yaxis_title="Suhu Laut (°C)", yaxis2_title="Klorofil (mg/m³)", legend=dict(x=1.1, y=1.1))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.write("### Fluktuasi Estimasi Stok Ikan (Biomassa)")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df["Nama_Bulan"], y=df["Estimasi_Stok"], name="Estimasi Stok", marker_color="cadetblue"))
    fig2.add_trace(go.Scatter(x=df["Nama_Bulan"], y=df["Estimasi_Stok"], mode="lines+markers", line=dict(color="orange"), name="Tren"))
    fig2.update_layout(xaxis_title="Bulan", yaxis_title="Estimasi Stok")
    st.plotly_chart(fig2, use_container_width=True)

# Tampilan tabel detail data mentah di bagian bawah
st.write("### Lihat Detail Data Mentah")
st.dataframe(df[["Bulan", "Nama_Bulan", "Suhu_Laut_C", "Klorofil", "Estimasi_Stok"]], use_container_width=True)
