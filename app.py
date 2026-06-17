import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Membaca data riil perairan barat Sumatra milik Anda
print("Membaca data riil Sumatra...")
df = pd.read_csv("Data Laut Samudra Hindia Barat Sumatra.csv")

# 2. Menentukan parameter model estimasi sesuai standar aplikasi
suhu_optimal = 28.50
alfa_klorofil = 3000
beta_penalti_suhu = 500

# 3. Menghitung rumus estimasi stok ikan bulanan
print("Menghitung estimasi stok ikan berdasarkan rumus model...")
# Menghitung selisih absolut suhu terhadap suhu optimal ikan
df["Penalti_Suhu"] = (df["Suhu_Laut_C"] - suhu_optimal).abs() * beta_penalti_suhu

# Rumus integrasi: (Luas Habitat * 1.5) + (Klorofil * Alfa) - Penalti Suhu
df["Estimasi_Stok"] = (df["Luas Habitat"] * 1.5) + (df["Klorofil"] * alfa_klorofil) - df["Penalti_Suhu"]

# Membulatkan hasil kalkulasi agar tidak ada angka desimal di belakang koma
df["Estimasi_Stok"] = df["Estimasi_Stok"].round(0).astype(int)

# 4. Menampilkan hasil kalkulasi ke layar console
print("\nHASIL ESTIMASI STOK IKAN PERAIRAN BARAT SUMATRA TAHUN 2025:")
print(df[["Nama_Bulan", "Suhu_Laut_C", "Klorofil", "Estimasi_Stok"]].to_string(index=False))

# 5. Membuat grafik visualisasi interaktif dua sumbu (Dual Axis)
print("\nMembuat grafik visualisasi interaktif...")
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Menambahkan grafik batang untuk Estimasi Stok Ikan
fig.add_trace(
    go.Bar(
        x=df["Nama_Bulan"],
        y=df["Estimasi_Stok"],
        name="Estimasi Stok (Biomassa)",
        marker_color="cadetblue"
    ),
    secondary_y=False
)

# Menambahkan grafik garis untuk Tren Klorofil
fig.add_trace(
    go.Scatter(
        x=df["Nama_Bulan"],
        y=df["Klorofil"],
        name="Klorofil_a (mg/m³)",
        mode="lines+markers",
        line=dict(color="green", width=2, dash="dash")
    ),
    secondary_y=True
)

# Mengatur tampilan tata letak (layout) grafik
fig.update_layout(
    title="Dashboard Analisis Estimasi Stok Ikan Berbasis Data Satelit Sumatra 2025",
    xaxis_title="Bulan",
    yaxis_title="Estimasi Stok (Biomassa)",
    yaxis2_title="Konsentrasi Klorofil_a (mg/m³)",
    hovermode="x unified",
    legend=dict(x=1.05, y=1)
)

# Menyimpan grafik menjadi file HTML dan membukanya otomatis di browser
fig.write_html("dashboard_estimasi_stok_sumatra.html")
print("Selesai! Grafik interaktif tersimpan dengan nama: dashboard_estimasi_stok_sumatra.html")
fig.show()
