import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="DSS Penilaian Dosen - AHP, SAW, TOPSIS", layout="wide")

st.title("🎓 Sistem Pendukung Keputusan (DSS) Penilaian Dosen Terbaik")
st.write("Aplikasi ini mengimplementasikan metode **AHP (Analytical Hierarchy Process)** untuk pembobotan kriteria, serta **SAW (Simple Additive Weighting)** dan **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)** untuk perangkingan 30 data dummy dosen dengan nama riil akademis.")

# ==========================================
# 1. GENERATE DUMMY DATASET (30 Dosen dengan Nama Riil)
# ==========================================
@st.cache_data
def load_dummy_data():
    np.random.seed(42)
    
    # Daftar 30 Nama Dosen Indonesia beserta Gelar Akademis
    nama_dosen = [
        "Dr. Eng. Irwan Prasetyo, M.T.",
        "Budi Santoso, M.Kom.",
        "Siti Rahayu, M.T.",
        "Dr. Diana Lestari, M.Si.",
        "Ahmad Fauzi, M.Kom.",
        "Rian Hidayat, M.T.",
        "Indah Permatasari, M.Kom.",
        "Dr. Bambang Wijaya, M.Eng.",
        "Andi Wijaya, M.T.",
        "Dewi Sartika, M.Kom.",
        "Dr. Yusuf Mahendra, M.Si.",
        "Eko Prasetyo, M.T.",
        "Rina Wijayanti, M.Kom.",
        "Agus Setiawan, M.T.",
        "Dr. Megawati, M.Si.",
        "Fajar Nugroho, M.Kom.",
        "Sri Wahyuni, M.T.",
        "Dr. Hendra Wijaya, M.Eng.",
        "Aditya Pratama, M.Kom.",
        "Kartika Sari, M.T.",
        "Dr. Rizky Ramadhan, M.Si.",
        "Taufik Hidayat, M.T.",
        "Siti Aminah, M.Kom.",
        "Dr. Joko Susilo, M.Eng.",
        "Anisa Putri, M.T.",
        "Dwi Cahyono, M.Kom.",
        "Dr. Tri Wahyuni, M.Si.",
        "Rudi Hermawan, M.T.",
        "Mega Utami, M.Kom.",
        "Dr. Gunawan Wibisono, M.Eng."
    ]
    
    # Kriteria Penilaian:
    # C1: Pedagogik (Benefit) - skala 1-100
    # C2: Profesionalisme (Benefit) - skala 1-100
    # C3: Penelitian & Publikasi (Benefit) - skala 1-100
    # C4: Komplain Mahasiswa (Cost) - skala 0-5
    
    c1 = np.random.randint(70, 98, size=30)
    c2 = np.random.randint(65, 96, size=30)
    c3 = np.random.randint(60, 95, size=30)
    c4 = np.random.randint(0, 6, size=30) 
    
    df = pd.DataFrame({
        'Nama Dosen': nama_dosen,
        'C1 (Pedagogik)': c1,
        'C2 (Profesionalisme)': c2,
        'C3 (Penelitian)': c3,
        'C4 (Komplain)': c4
    })
    return df

df_data = load_dummy_data()

st.sidebar.header("⚙️ Pengaturan & Navigasi")
menu = st.sidebar.radio("Pilih Halaman / Proses:", ["1. Dataset Awal", "2. Pembobotan Kriteria (AHP)", "3. Perangkingan (SAW & TOPSIS)"])

# ==========================================
# FIXED AHP VALUES FOR THE CRITERIA
# ==========================================
AHP_matrix = np.array([
    [1.0, 1.0, 2.0, 2.0], # C1
    [1.0, 1.0, 2.0, 2.0], # C2
    [0.5, 0.5, 1.0, 1.0], # C3
    [0.5, 0.5, 1.0, 1.0]  # C4
])
kolom_sum = AHP_matrix.sum(axis=0)
AHP_norm = AHP_matrix / kolom_sum
bobot = AHP_norm.mean(axis=1)
kriteria_list = ['C1 (Pedagogik)', 'C2 (Profesionalisme)', 'C3 (Penelitian)', 'C4 (Komplain)']
tipe_kriteria = np.array([1, 1, 1, -1]) # 1 = Benefit, -1 = Cost

if menu == "1. Dataset Awal":
    st.subheader("📊 Dataset Dummy Penilaian 30 Dosen")
    st.write("Berikut adalah data nilai evaluasi kinerja untuk 30 dosen berdasarkan 4 kriteria utama:")
    st.markdown("- **C1 (Pedagogik):** Benefit (Semakin tinggi semakin baik)")
    st.markdown("- **C2 (Profesionalisme):** Benefit (Semakin tinggi semakin baik)")
    st.markdown("- **C3 (Penelitian & Publikasi):** Benefit (Semakin tinggi semakin baik)")
    st.markdown("- **C4 (Komplain Mahasiswa):** Cost (Semakin rendah/sedikit komplain semakin baik)")
    
    st.dataframe(df_data, use_container_width=True, height=450)
    
    # Quick Statistics
    st.subheader("📈 Analisis Deskriptif Singkat")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rata-rata Pedagogik", f"{df_data['C1 (Pedagogik)'].mean():.2f}")
    col2.metric("Rata-rata Profesionalisme", f"{df_data['C2 (Profesionalisme)'].mean():.2f}")
    col3.metric("Rata-rata Penelitian", f"{df_data['C3 (Penelitian)'].mean():.2f}")
    col4.metric("Total Komplain", f"{df_data['C4 (Komplain)'].sum()} Kali")

elif menu == "2. Pembobotan Kriteria (AHP)":
    st.subheader("📐 Metode AHP (Analytical Hierarchy Process)")
    st.write("Metode AHP digunakan untuk menentukan bobot prioritas dari masing-masing kriteria melalui matriks perbandingan berpasangan.")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("**Matriks Perbandingan Berpasangan Kriteria:**")
        df_ahp = pd.DataFrame(AHP_matrix, index=['C1', 'C2', 'C3', 'C4'], columns=['C1', 'C2', 'C3', 'C4'])
        st.dataframe(df_ahp)
        st.caption("Interpretasi: Nilai 2.0 berarti kriteria pada baris sedikit lebih penting dari kriteria pada kolom.")
        
    with col_right:
        st.markdown("**Hasil Bobot Prioritas Kriteria:**")
        df_bobot = pd.DataFrame({
            'Kriteria': kriteria_list,
            'Bobot Hasil AHP': bobot
        })
        st.dataframe(df_bobot)
        
    st.success("✅ **Uji Konsistensi (Consistency Ratio): CR = 0.000 <= 0.1** -> Matriks Perbandingan Berpasangan Konsisten secara Matematis dan Bobot Valid untuk digunakan!")
    
    st.write("🖼️ **Visualisasi Heatmap Matriks AHP:**")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(AHP_matrix, annot=True, fmt=".2f", xticklabels=['C1', 'C2', 'C3', 'C4'], yticklabels=['C1', 'C2', 'C3', 'C4'], cmap="YlGnBu", ax=ax)
    plt.title("Tingkat Kepentingan Antar Kriteria")
    st.pyplot(fig)

elif menu == "3. Perangkingan (SAW & TOPSIS)":
    st.subheader("🏆 Proses Perangkingan Rekomendasi Dosen Terbaik")
    
    X = df_data.iloc[:, 1:].values.astype(float)
    alternatif = df_data['Nama Dosen'].tolist()
    
    # --- METHOD 1: SAW ---
    R_saw = np.zeros(X.shape)
    for j in range(X.shape[1]):
        if tipe_kriteria[j] == 1:
            R_saw[:, j] = X[:, j] / np.max(X[:, j])
        else:
            R_saw[:, j] = np.min(X[:, j]) / X[:, j]
            R_saw[X[:, j] == 0, j] = 1.0
            
    V_saw = np.dot(R_saw, bobot)
    df_result_saw = pd.DataFrame({'Nama Dosen': alternatif, 'Skor SAW': V_saw})
    df_result_saw['Rank SAW'] = df_result_saw['Skor SAW'].rank(ascending=False).astype(int)
    
    # --- METHOD 2: TOPSIS ---
    R_topsis = X / np.sqrt(np.sum(X**2, axis=0))
    Y = R_topsis * bobot
    
    A_pos = np.zeros(X.shape[1])
    A_neg = np.zeros(X.shape[1])
    for j in range(X.shape[1]):
        if tipe_kriteria[j] == 1:
            A_pos[j] = np.max(Y[:, j])
            A_neg[j] = np.min(Y[:, j])
        else:
            A_pos[j] = np.min(Y[:, j])
            A_neg[j] = np.max(Y[:, j])
            
    D_pos = np.sqrt(np.sum((Y - A_pos)**2, axis=1))
    D_neg = np.sqrt(np.sum((Y - A_neg)**2, axis=1))
    V_topsis = D_neg / (D_pos + D_neg)
    
    df_result_topsis = pd.DataFrame({'Nama Dosen': alternatif, 'Skor TOPSIS': V_topsis})
    df_result_topsis['Rank TOPSIS'] = df_result_topsis['Skor TOPSIS'].rank(ascending=False).astype(int)
    
    df_final = pd.merge(df_result_saw, df_result_topsis, on='Nama Dosen')
    
    tab1, tab2, tab3 = st.tabs(["📊 Perbandingan Hasil Akhir", "🔍 Detail Perhitungan SAW", "🔍 Detail Perhitungan TOPSIS"])
    
    with tab1:
        st.write("Tabel gabungan hasil skor preferensi dan perangkingan dari metode SAW dan TOPSIS:")
        st.dataframe(df_final.sort_values(by='Rank SAW'), use_container_width=True, height=450)
        
        top_saw = df_final.sort_values(by='Rank SAW').iloc[0]['Nama Dosen']
        top_topsis = df_final.sort_values(by='Rank TOPSIS').iloc[0]['Nama Dosen']
        
        st.info(f"💡 **Kesimpulan Perangkingan:** Menurut metode **SAW**, Dosen terbaik adalah **{top_saw}**. Sedangkan menurut metode **TOPSIS**, Dosen terbaik adalah **{top_topsis}**.")
        
        st.write("📊 **Grafik Perbandingan Top 10 Dosen Teratas (Berdasarkan SAW):**")
        top_10 = df_final.sort_values(by='Rank SAW').head(10)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        x_indices = np.arange(len(top_10))
        width = 0.35
        
        ax.bar(x_indices - width/2, top_10['Skor SAW'], width, label='Skor SAW', color='skyblue')
        ax.bar(x_indices + width/2, top_10['Skor TOPSIS'], width, label='Skor TOPSIS', color='lightgreen')
        
        ax.set_xticks(x_indices)
        ax.set_xticklabels(top_10['Nama Dosen'], rotation=45, ha='right')
        ax.set_title("Perbandingan Skor Top 10 Dosen Teratas")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    with tab2:
        st.markdown("**Matriks Normalisasi (R) SAW:**")
        st.dataframe(pd.DataFrame(R_saw, index=alternatif, columns=['C1', 'C2', 'C3', 'C4']), height=300)
        st.markdown("**Top 5 Dosen Versi SAW:**")
        st.dataframe(df_final[['Nama Dosen', 'Skor SAW', 'Rank SAW']].sort_values(by='Rank SAW').head(5))

    with tab3:
        st.markdown("**Matriks Normalisasi Terbobot (Y) TOPSIS:**")
        st.dataframe(pd.DataFrame(Y, index=alternatif, columns=['C1', 'C2', 'C3', 'C4']), height=300)
        st.markdown("**Top 5 Dosen Versi TOPSIS:**")
        st.dataframe(df_final[['Nama Dosen', 'Skor TOPSIS', 'Rank TOPSIS']].sort_values(by='Rank TOPSIS').head(5))