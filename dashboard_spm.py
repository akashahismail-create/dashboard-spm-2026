import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Pengurusan SPM NEGERI SELANGOR", layout="wide")

# ===== HILANGKAN BAR STREAMLIT + BG BIRU MUDA =====
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    .stApp {background-color: #E6F3FF;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df_jadual = pd.read_excel('JADUAL PEPERISAAN SPM 2026.xlsx')
        df_nama = pd.read_excel('nama sekolah.xlsx')
        df_pusat = pd.read_excel('senarai pusat.xlsx')
        df_bilik = pd.read_excel('senarai bilik kebal.xls')
    except FileNotFoundError as e:
        st.error(f"File tak jumpa: {e}. Sila upload ke Github")
        st.stop()

    for df in [df_jadual, df_nama, df_pusat, df_bilik]:
        df.columns = df.columns.str.upper().str.strip()

    df_temp = pd.merge(df_jadual, df_pusat, on='KOD MATA PELAJARAN', how='left')
    df_full = pd.merge(df_temp, df_nama, on='NO PUSAT', how='left')
    return df_jadual, df_nama, df_pusat, df_bilik, df_full

df_jadual, df_nama, df_pusat, df_bilik, df_full = load_data()

NAMA_ADMIN = "Akashah bin Ismail"
JAWATAN_ADMIN = "Pegawai meja SPM Negeri Selangor"

# ===== HEADER =====
col_logo, col_title = st.columns([1, 5])
with col_logo: 
    st.image("logo.png", width=200)
with col_title:
    st.title(" Dashboard Pengurusan SPM 2026")
    st.write(f"**Nama:** {NAMA_ADMIN}")
    st.write(f"**Jawatan:** {JAWATAN_ADMIN}")

st.write("---")

col1, col2, col3 = st.columns(3)
with col1: st.metric("Jumlah Pusat", df_nama['NO PUSAT'].nunique())
with col2: st.metric("Jumlah Bilik Kebal", len(df_bilik))
with col3: st.metric("Jumlah Subjek", df_jadual['KOD MATA PELAJARAN'].nunique())

st.markdown("---")

# ===== LINK =====
LINK_CALON = "https://script.google.com/macros/s/AKfycbwav3jbWQEkTW2yTK9PnanlItxPM5NpCHADLNb_BRjY4hmsale257tSqMsRTdqv88HA/exec"
LINK_PENGURUSAN = "https://drive.google.com/drive/folders/193ELWVyPDORTVE7ZSVe2B3rsZILkg7f6?usp=drive_link"

PASSWORD = "spmB" # Tukar password sini je

col_kosong, col_butang1, col_butang2 = st.columns([3, 1, 1])

with col_butang1:
    if st.button("📝 CALON", key="btn_calon", use_container_width=True, type="primary"):
        st.session_state.show_pw_calon = True

with col_butang2:
    if st.button("📊 PENGURUSAN SPM", key="btn_urus", use_container_width=True, type="secondary"):
        st.session_state.show_pw_urus = True

# ===== POPUP PASSWORD UNTUK CALON =====
if st.session_state.get("show_pw_calon", False):
    with st.form("form_password_calon"):
        st.write("### 🔒 Password Portal CALON")
        pw = st.text_input("Masukkan Password", type="password", key="pw_calon")
        col1, col2 = st.columns(2)
        with col1: submit = st.form_submit_button("Masuk")
        with col2: cancel = st.form_submit_button("Batal")

        if submit:
            if pw == PASSWORD:
                st.session_state.show_pw_calon = False
                st.success("Password betul!")
                st.link_button("🚀 BUKA PORTAL CALON", LINK_CALON, use_container_width=True, type="primary")
            else:
                st.error("Password salah!")
        if cancel:
            st.session_state.show_pw_calon = False

# ===== POPUP PASSWORD UNTUK PENGURUSAN =====
if st.session_state.get("show_pw_urus", False):
    with st.form("form_password_urus"):
        st.write("### 🔒 Password Folder PENGURUSAN")
        pw = st.text_input("Masukkan Password", type="password", key="pw_urus")
        col1, col2 = st.columns(2)
        with col1: submit = st.form_submit_button("Masuk")
        with col2: cancel = st.form_submit_button("Batal")

        if submit:
            if pw == PASSWORD:
                st.session_state.show_pw_urus = False
                st.success("Password betul!")
                st.link_button("🚀 BUKA FOLDER PENGURUSAN", LINK_PENGURUSAN, use_container_width=True, type="secondary")
            else:
                st.error("Password salah!")
        if cancel:
            st.session_state.show_pw_urus = False

st.write("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏫 Senarai Pusat", "🔒 Senarai Bilik Kebal", "📅 Jadual", "🔍 Carian", "📈 Analisis"])

with tab1:
    st.subheader("Senarai Pusat Peperiksaan")
    st.dataframe(df_nama, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Senarai Bilik Kebal")
    st.dataframe(df_bilik, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Jadual Peperiksaan + Maklumat Pusat")
    st.dataframe(df_full, use_container_width=True, hide_index=True)

with tab4:
    st.subheader("🔍 Carian Mengikut Sekolah")
    st.write("Cari jadual peperiksaan berdasarkan **Nama Sekolah**")
    
    col_cari1, col_cari2 = st.columns([2, 1])
    
    with col_cari1:
        carian_sekolah = st.text_input(
            "1. Nama Sekolah", 
            placeholder="Contoh: SMK KEBANGSAAN SUBANG JAYA atau SUBANG"
        )
    
    with col_cari2:
        pilihan_kertas = st.selectbox(
            "2. Pilih Kertas", 
            options=["Semua", "1", "2", "3", "4"],
            index=0
        )
    
    if carian_sekolah:
        # Filter ikut NAMA SEKOLAH dulu
        mask_sekolah = df_full['NAMA SEKOLAH'].astype(str).str.contains(carian_sekolah, case=False, na=False)
        hasil_mp = df_full[mask_sekolah]
        
        # Filter ikut kertas pulak kalau pilih selain "Semua"
        if pilihan_kertas != "Semua":
            if 'KERTAS' in hasil_mp.columns:
                hasil_mp = hasil_mp[hasil_mp['KERTAS'].astype(str).str.contains(pilihan_kertas, case=False, na=False)]
            else:
                st.warning("Column 'KERTAS' tak dijumpai dalam excel. Sila check nama column.")

        if not hasil_mp.empty:
            st.success(f"✅ Dijumpai **{len(hasil_mp)} jadual** untuk '{carian_sekolah}' Kertas {pilihan_kertas}")
            st.dataframe(hasil_mp, use_container_width=True, hide_index=True)
        else:
            st.warning(f"❌ Tiada data untuk sekolah: '{carian_sekolah}'")
    else:
        st.info("Sila masukkan Nama Sekolah untuk mula mencari")

with tab5:
    st.subheader("Analisis Ringkas")
    if 'KOD KAWASAN' in df_pusat.columns:
        st.bar_chart(df_pusat['KOD KAWASAN'].value_counts())

st.write("---")
st.caption("akashah ismail")
