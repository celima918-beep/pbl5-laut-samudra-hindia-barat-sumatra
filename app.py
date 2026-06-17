import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Estimasi Stok Ikan Sumatra", layout="wide")

st.title("🐟 Estimasi Stok Ikan Berbasis Data Satelit")
st.write("Simulasi integrasi data oseanografi Suhu dan Klorofil untuk memprediksi fluktuasi biomassa perairan barat Sumatra.")

# 1. Membaca data dari file CSV riil Anda
# Program menggunakan nama file yang Anda unggah ke GitHub
try:
    df_awal = pd.read_csv("Data Laut Samudra Hindia Barat Sumatra.csv")
    
    # Menghapus kolom kelima (Luas Habitat) agar tidak masuk ke pemrosesan
    # iloc[:, 4] merujuk pada kolom indeks ke 4 alias kolom kelima
    kolom_kelima = df_awal.columns[4]
    df = df_awal.drop(columns=[kolom_kelima])
except Exception as e:
    st.error(f"Gagal membaca file CSV. Pastikan file 'Data Laut Samudra Hindia Barat Sumatra.csv' sudah diunggah ke GitHub. Error: {e}")
    st.stop()

# 2. Membuat panel input parameter model estimasi di sebelah kiri
st.sidebar.header("Parameter Model Estimasi")
st.sidebar.write("Sesuaikan sensitivitas ikan terhadap lingkungan:")

suhu_optimal = st.sidebar.slider("Suhu Optimal Ikan (°C)", 25.00, 35.00, 28.50, 0.10)
alfa_klorofil = st.sidebar.slider("Faktor Pengali Klorofil (α)", 500, 5000, 3000, 100)
beta_penalti_suhu = st.sidebar.slider("Faktor Penalti Suhu (β)", 100, 1000, 500, 50)

# 3. Menghitung rumus estimasi stok ikan secara otomatis
# Karena kolom kelima tidak dimasukkan, kita menggunakan nilai konstan 1000 untuk perhitungan rumus
luas_konstan = 1000
df["Penalti_Suhu"] = (df["Suhu_Laut_C"] - suhu_optimal).abs() * beta_penalti_suhu
df["Estimasi_Stok"] = (luas_konstan * 1.5) + (df["Klorofil"] * alfa_klorofil) - df["Penalti_Suhu"]
df["Estimasi_Stok"] = df["Estimasi_Stok"].round(0).astype(int)

# 4. Membuat tampilan visualisasi grafik atas
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

# 5. Tampilan tabel detail data mentah di bagian bawah tanpa kolom kelima
st.write("### Lihat Detail Data Mentah (Tanpa Kolom Kelima)")
st.dataframe(df[["Bulan", "Nama_Bulan", "Suhu_Laut_C", "Klorofil", "Estimasi_Stok"]], use_container_width=True)
