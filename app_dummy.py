from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci_rahasia_literasi_2024'

# --- HELPER FUNCTION: LOAD DATA ---
def load_data():
    """
    Membaca semua file CSV dari folder data_dummy dan mengembalikannya sebagai DataFrame.
    Pastikan file: 'dim_buku.csv', 'dim_siswa.csv', 'fact_aktivitas_baca.csv' ada di folder data_dummy.
    """
    base_path = os.path.join(os.getcwd(), 'data_dummy')
    
    try:
        df_buku = pd.read_csv(os.path.join(base_path, 'dim_buku.csv'))
        df_siswa = pd.read_csv(os.path.join(base_path, 'dim_siswa.csv'))
        df_fact = pd.read_csv(os.path.join(base_path, 'fact_aktivitas_baca.csv'))
        return df_buku, df_siswa, df_fact
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None

# --- ROUTE ---
@app.route('/')
def home():
    df_buku, df_siswa, df_fact = load_data()
    
    if df_buku is None:
        return "Error: File CSV tidak ditemukan di folder data_dummy."

    # --- 1. KPI CARDS (Statistik Utama) ---
    total_siswa = len(df_siswa)
    total_buku = len(df_buku)
    total_durasi_jam = round(df_fact['durasi_menit'].sum() / 60, 1)
    total_halaman = df_fact['halaman_selesai'].sum()

    # --- 2. DATA PROCESSING UNTUK GRAFIK ---
    
    # Grafik 1: Top 5 Buku Terpopuler (Berdasarkan frekuensi baca)
    top_buku = df_fact['id_buku'].value_counts().reset_index()
    top_buku.columns = ['id_buku', 'jumlah_baca']
    # Gabungkan dengan tabel buku untuk dapat judul
    top_buku = top_buku.merge(df_buku, on='id_buku')
    top_buku = top_buku.sort_values('jumlah_baca', ascending=False).head(5)
    
    chart_buku_labels = top_buku['judul_buku'].tolist()
    chart_buku_data = top_buku['jumlah_baca'].tolist()

    # Grafik 2: Aktivitas Baca per Kelas
    # Gabungkan fakta dengan siswa
    merged_siswa = df_fact.merge(df_siswa, on='id_siswa')
    kelas_stats = merged_siswa.groupby('kelas')['durasi_menit'].sum().reset_index()
    
    chart_kelas_labels = [f"Kelas {k}" for k in kelas_stats['kelas'].tolist()]
    chart_kelas_data = kelas_stats['durasi_menit'].tolist()

    # Grafik 3: Trend Harian (7 Hari Terakhir di data)
    # Konversi tanggal dan urutkan
    df_fact['tanggal_baca'] = pd.to_datetime(df_fact['tanggal_baca'])
    daily_stats = df_fact.groupby('tanggal_baca')['durasi_menit'].sum().reset_index()
    daily_stats = daily_stats.sort_values('tanggal_baca')
    
    # Ambil format string tanggal untuk chart
    chart_trend_labels = daily_stats['tanggal_baca'].dt.strftime('%Y-%m-%d').tolist()
    chart_trend_data = daily_stats['durasi_menit'].tolist()

    return render_template('dashboard_dummy.html', 
                           kpi={
                               'siswa': total_siswa, 
                               'buku': total_buku, 
                               'durasi': total_durasi_jam,
                               'halaman': total_halaman
                           },
                           chart_buku={'labels': chart_buku_labels, 'data': chart_buku_data},
                           chart_kelas={'labels': chart_kelas_labels, 'data': chart_kelas_data},
                           chart_trend={'labels': chart_trend_labels, 'data': chart_trend_data}
                           )

@app.route('/buku_table')
def buku_table():
    df_buku, _, _ = load_data()
    return render_template('buku_table.html', books=df_buku.to_dict(orient='records'))

@app.route('/siswa_table')
def siswa_table():
    _, df_siswa, _ = load_data()
    return render_template('siswa_table.html', students=df_siswa.to_dict(orient='records'))

@app.route('/aktivitasbaca_table')
def aktivitasbaca_table():
    _, _, df_fact = load_data()
    # Batasi 100 data saja biar tidak berat loadingnya
    return render_template('aktivitasbaca_table.html', activities=df_fact.head(100).to_dict(orient='records'))

@app.route('/login')
def login():
    # Render template login jika ada, atau return string biasa
    try:
        return render_template('login.html')
    except:
        return "Halaman Login (Dummy)"

@app.route('/register')
def register():
    try:
        return render_template('register.html')
    except:
        return "Halaman Register (Dummy)"

if __name__ == '__main__':
    app.run(debug=True)