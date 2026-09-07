import streamlit as st
import pandas as pd

# ===== 1. SETTING PAGE =====
st.set_page_config(
    page_title="Dashboard SPM 2026",
    page_icon="📊",
    layout="wide"
)

# ===== 2. SEMBUNYIKAN MAHKOTA + SETTING GAMBAR BERPUSING =====
st.markdown("""
<style>
    /* Sembunyikan toolbar mahkota */
    [data-testid="stToolbar"] {
        display: none;
    }
    /* Kod untuk gambar berpusing */
    .berpusing {
        animation: spin 4s linear infinite;
        width: 120px;
        display: block;
        margin: auto;
        margin-bottom: 10px;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    /* Title cantik sikit */
    .title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# ===== 3. HEADER + LOGO BERPUSING =====
# TUKAR LINK NI DENGAN LINK LOGO SEKOLAH AWAK
logo_url = "https://upload.wikimedia.org/wikipedia/commons/a7/React-icon.svg" 

st.markdown(f'<img src="{logo_url}" class="berpusing">', unsafe_allow_html=True)
st.markdown('<p class="title">DASHBOARD ANALISIS SPM 2026</p>', unsafe_allow_html=True)
st.markdown("---")

# ===== 4. CONTOH DATA KOSONG - AWAK TUKAR DENGAN DATA BENAR =====
data = {
    'Mata Pelajaran': ['BM', 'BI', 'MATEMATIK', 'SAINS', 'SEJARAH'],
    'Bil. A+': [15, 10, 8, 12, 20],
    'Bil. Lulus': [80, 75, 70, 78, 90],
    'Gred Purata': [3.2, 3.5, 4.1, 3.8, 2.9]
}
df = pd.DataFrame(data)

# ===== 5. PAPARKAN DATA =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Bilangan Lulus Mengikut Subjek")
    st.bar_chart(df.set_index('Mata Pelajaran')['Bil. Lulus'])

with col2:
    st.subheader("📊 Jadual Keputusan")
    st.dataframe(df, use_container_width=True)

# ===== 6. FOOTER =====
st.markdown("---")
st.caption("Dibangunkan oleh: Puan Akashah | Kemaskini Terakhir: Sept 2026")
