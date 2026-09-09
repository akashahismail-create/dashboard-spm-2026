import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Pengurusan SPM NEGERI SELANGOR", layout="wide")

# HILANGKAN BAR STREAMLIT
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #E6F3FF;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df_jadual = pd.read_excel('JADUAL PEPERISAAN SPM 2026.xlsx')
    df_nama = pd.read_excel('nama sekolah.xlsx')
    df_pusat = pd.read_excel('senarai pusat.xlsx')
    df_bilik = pd.read_excel('senarai bilik kebal.xls')
    for df in [df_jadual, df_nama, df_pusat, df_bilik]:
        df.columns = df.columns.str.upper().str.strip()
    df_temp = pd.merge(df_jadual, df_pusat, on='KOD MATA PELAJARAN', how='left')
    df_full = pd.merge(df_temp, df_nama, on='NO PUSAT', how='left')
    return df_jadual, df_nama, df_pusat, df_bilik, df_full

df_jadual, df_nama, df_pusat, df_bilik, df_full = load_data()

col_logo, col_title = st.columns([1, 5])
with col_logo: st.image("logo.png", width=200)
with col_title:
    st.title(" Dashboard Pengurusan SPM 2026")
    st.write("**Nama:** Akashah bin Ismail")
    st.write("**Jawatan:** Pegawai meja SPM Negeri Selangor")

st.write("---")

col1, col2, col3 = st.columns(3)
with col1: st.metric("Jumlah Pusat", df_nama['NO PUSAT'].nunique())
with col2: st.metric("Jumlah Bilik Kebal", len(df_bilik))
with col3: st.metric("Jumlah Subjek", df_jadual['KOD MATA PELAJARAN'].nunique())

st.markdown("---")

# ===== INI BAHAGIAN PENTING =====
LINK_CALON = "https://script.google.com/macros/s/AKfycbwav3jbWQEkTW2yTK9PnanlItxPM5NpCHADLNb_BRjY4hmsale257tSqMsRTdqv88HA/exec"
LINK_PENGURUSAN = "https://drive.google.com/drive/folders/193ELWVyPDORTVE7ZSVe2B3rsZILkg7f6?usp=drive_link"

col_kosong, col_butang1, col_butang2 = st.columns([3, 1, 1])
with col_butang1:
    st.link_button("📝 CALON", LINK_CALON, use_container_width=True, type="primary")
with col_butang2:
    st.link_button("📊 PENGURUSAN SPM", LINK_PENGURUSAN, use_container_width=True, type="secondary")
# ===== HABIS BAHAGIAN PENTING =====

st.write("---")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏫 Senarai Pusat", "🔒 Senarai Bilik Kebal", "📅 Jadual", "🔍 Carian", "📈 Analisis"])

with tab1: st.dataframe(df_nama, use_container_width=True, hide_index=True)
with tab2: st.dataframe(df_bilik, use_container_width=True, hide_index=True)
with tab3: st.dataframe(df_full, use_container_width=True, hide_index=True)

st.caption("akashah ismail")
