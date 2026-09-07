import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Pengurusan SPM NEGERI SELANGOR", layout="wide")

# ===== SEMBUNYI BUTTON FORK + GITHUB + FOOTER START =====
st.markdown("""
<style>
#MainMenu {visibility: hidden;} /* Sembunyi menu 3 titik */
header {visibility: hidden;} /* Sembunyi bar atas Fork + Github */
footer {visibility: hidden;} /* Sembunyi "Made with Streamlit" kat bawah */
</style>
""", unsafe_allow_html=True)
# ===== HABIS =====

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

    if 'TARIKH' in df_full.columns:
        df_full['TARIKH'] = pd.to_datetime(df_full['TARIKH'], errors='coerce')

    return df_jadual, df_nama, df_pusat, df_bilik, df_full

df_jadual, df_nama, df_pusat, df_bilik, df_full = load_data()
st.markdown("---") # Garisan pemisah

st.markdown("---")

st.markdown("---")
NAMA_ADMIN = "Akashah_bin_Ismail"
JAWATAN_ADMIN = "Pegawai_Meja_SPM_Negeri_Selangor"

# ===== BAHAGIAN HEADER + LOGO =====
col_logo, col_title = st.columns([1, 5])

with col_logo:
    # GAMBAR YANG KAU UPLOAD TADI
    st.image("logo.png", width=100)

with col_title:
    # TUKAR WARNA BACKGROUND
    st.markdown("""
    <style>
   .stApp {
        background-color: #E6F3FF; /* Warna biru muda */
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Dashboard Pengurusan SPM 2026")
    st.write(f"**Nama:** {NAMA_ADMIN} | **Jawatan:** {JAWATAN_ADMIN}")

st.write("---")
# ===== HABIS HEADER =====

col1, col2, col3 = st.columns(3)
with col1: st.metric("Jumlah Pusat", df_nama['NO PUSAT'].nunique())
with col2: st.metric("Jumlah Bilik Kebal", len(df_bilik))
with col3: st.metric("Jumlah Subjek", df_jadual['KOD MATA PELAJARAN'].nunique())

# BUTTON PENGURUSAN CALON
st.markdown("---")

# BUAT 2 KOLUM: Kiri kosong, Kanan butang
col_kosong, col_butang = st.columns([4, 1])

with col_butang:
    if st.button("📝 CALON", key="btn_calon", use_container_width=True, type="primary"):
        st.session_state.show_pw = True

if st.session_state.get("show_pw", False):
    with st.form("form_password"):
        st.write("### 🔒 Masukkan Password")
        pw = st.text_input("Password", type="password")
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Masuk")
        with col2:
            cancel = st.form_submit_button("Batal")

        if submit:
            if pw == "spmB": # <--- TUKAR PASSWORD SINI
                st.session_state.show_pw = False
                st.markdown('<meta http-equiv="refresh" content="0; url=https://script.google.com/macros/s/AKfycbwav3jbWQEkTW2yTK9PnanlItxPM5NpCHADLNb_BRjY4hmsale257tSqMsRTdqv88HA/exec">', unsafe_allow_html=True)
                st.success("Password betul! Membuka...")
            else:
                st.error("Password salah!")
        if cancel:
            st.session_state.show_pw = False

st.write("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏫 Senarai Pusat", "🔒 Senarai Bilik Kebal", "📅 Jadual + Pusat", "🔍 Carian", "📈 Analisis"
])

with tab1:
    st.subheader("Senarai Pusat Peperiksaan")
    st.dataframe(df_nama, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Senarai Bilik Kebal")
    st.dataframe(df_bilik, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Jadual Peperiksaan + Maklumat Pusat")
    want = ['TARIKH', 'HARI', 'KOD MATA PELAJARAN', 'MATA PELAJARAN', 'NO PUSAT', 'NAMA PUSAT', 'KOD KAWASAN']
    cols = [c for c in want if c in df_full.columns]
    st.dataframe(df_full[cols].drop_duplicates().sort_values('TARIKH'), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("🔍 Carian Mata Pelajaran + No Kertas")
    carian_mp = st.text_input("Langkah 1: Cari Kod atau Nama Mata Pelajaran", placeholder="cth: 1119 atau SEJARAH")

    if carian_mp:
        mask_kod = df_full['KOD MATA PELAJARAN'].astype(str).str.contains(carian_mp, case=False, na=False)
        mask_nama = df_full['MATA PELAJARAN'].astype(str).str.contains(carian_mp, case=False, na=False)
        hasil_mp = df_full[mask_kod | mask_nama]

        if not hasil_mp.empty:
            kod = hasil_mp['KOD MATA PELAJARAN'].iloc[0]
            nama_mp = hasil_mp['MATA PELAJARAN'].iloc[0]
            st.success(f"Mata Pelajaran: **{kod} - {nama_mp}**")

            if 'NO KERTAS' in hasil_mp.columns:
                senarai_kertas = sorted(hasil_mp['NO KERTAS'].dropna().unique())
                carian_kertas = st.selectbox("Langkah 2: Pilih No Kertas", options=['Semua'] + [str(x) for x in senarai_kertas])
                hasil_akhir = hasil_mp if carian_kertas == 'Semua' else hasil_mp[hasil_mp['NO KERTAS'].astype(str) == str(carian_kertas)]
            else:
                hasil_akhir = hasil_mp

            st.write(f"Jumlah Pusat: **{hasil_akhir['NO PUSAT'].nunique()}**")
            display_cols = ['NO PUSAT', 'NAMA PUSAT', 'KOD KAWASAN', 'NO KERTAS']
            display_cols = [c for c in display_cols if c in hasil_akhir.columns]
            st.dataframe(hasil_akhir[display_cols].drop_duplicates().sort_values('NO PUSAT'), use_container_width=True, hide_index=True)
        else:
            st.warning(f"Tiada pusat menawarkan: '{carian_mp}'")

with tab5:
    st.subheader("Analisis Ringkas")
    if 'KOD KAWASAN' in df_pusat.columns:
        st.bar_chart(df_pusat['KOD KAWASAN'].value_counts())

st.write("---")
st.caption("Dashboard SPM 2026")
