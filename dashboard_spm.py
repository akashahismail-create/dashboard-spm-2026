import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Dashboard Pengurusan SPM NEGERI SELANGOR", layout="wide")

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

    # MERGE UNTUK DAPAT DAERAH
    if 'KOD KAWASAN' in df_pusat.columns and 'KOD KAWASAN' in df_bilik.columns:
        df_pusat = pd.merge(df_pusat, df_bilik[['KOD KAWASAN', 'DAERAH']], on='KOD KAWASAN', how='left')

    df_temp = pd.merge(df_jadual, df_pusat, on='KOD MATA PELAJARAN', how='left')
    df_full = pd.merge(df_temp, df_nama, on='NO PUSAT', how='left')
    
    if 'TARIKH' in df_full.columns:
        df_full['TARIKH'] = pd.to_datetime(df_full['TARIKH'], errors='coerce')
        
    return df_jadual, df_nama, df_pusat, df_bilik, df_full

df_jadual, df_nama, df_pusat, df_bilik, df_full = load_data()

NAMA_ADMIN = "Akashah bin Ismail"
JAWATAN_ADMIN = "Pegawai meja SPM Negeri Selangor"

col_logo, col_title = st.columns([1, 5])
with col_logo: st.image("logo.png", width=200)
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

LINK_CALON = "https://script.google.com/macros/s/AKfycbwav3jbWQEkTW2yTK9PnanlItxPM5NpCHADLNb_BRjY4hmsale257tSqMsRTdqv88HA/exec"
LINK_PENGURUSAN = "https://drive.google.com/drive/folders/193ELWVyPDORTVE7ZSVe2B3rsZILkg7f6?usp=drive_link"
PASSWORD = "spmB"

col_kosong, col_butang1, col_butang2 = st.columns([3, 1, 1])
with col_butang1:
    if st.button("📝 CALON", key="btn_calon", use_container_width=True, type="primary"): st.session_state.show_pw_calon = True
with col_butang2:
    if st.button("📊 PENGURUSAN SPM", key="btn_urus", use_container_width=True, type="secondary"): st.session_state.show_pw_urus = True

if st.session_state.get("show_pw_calon", False):
    with st.form("form_password_calon"):
        st.write("### 🔒 Password Portal CALON")
        pw = st.text_input("Masukkan Password", type="password", key="pw_calon")
        col1, col2 = st.columns(2)
        with col1: submit = st.form_submit_button("Masuk")
        with col2: cancel = st.form_submit_button("Batal")
        if submit:
            if pw == PASSWORD: st.session_state.show_pw_calon = False; st.success("Password betul!"); st.link_button("🚀 BUKA PORTAL CALON", LINK_CALON, use_container_width=True, type="primary")
            else: st.error("Password salah!")
        if cancel: st.session_state.show_pw_calon = False

if st.session_state.get("show_pw_urus", False):
    with st.form("form_password_urus"):
        st.write("### 🔒 Password Folder PENGURUSAN")
        pw = st.text_input("Masukkan Password", type="password", key="pw_urus")
        col1, col2 = st.columns(2)
        with col1: submit = st.form_submit_button("Masuk")
        with col2: cancel = st.form_submit_button("Batal")
        if submit:
            if pw == PASSWORD: st.session_state.show_pw_urus = False; st.success("Password betul!"); st.link_button("🚀 BUKA FOLDER PENGURUSAN", LINK_PENGURUSAN, use_container_width=True, type="secondary")
            else: st.error("Password salah!")
        if cancel: st.session_state.show_pw_urus = False

st.write("---")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏫 Senarai Pusat", "🔒 Senarai Bilik Kebal", "📅 Jadual", "🔍 Carian", "📈 Analisis", "✏️ Edit Data"])

with tab1: st.subheader("Senarai Pusat Peperiksaan"); st.dataframe(df_nama, use_container_width=True, hide_index=True)
with tab2: st.subheader("Senarai Bilik Kebal"); st.dataframe(df_bilik, use_container_width=True, hide_index=True)
with tab3: st.subheader("Jadual Peperiksaan + Maklumat Pusat"); st.dataframe(df_full, use_container_width=True, hide_index=True)

with tab4:
    st.subheader("🔍 Carian Mata Pelajaran")
    col_cari1, col_cari2, col_cari3 = st.columns([2, 1, 1])
    with col_cari1: carian_mp = st.text_input("1. Kod Mata Pelajaran", placeholder="Contoh: 1103")
    with col_cari2: pilihan_kertas = st.selectbox("2. Pilih Kertas", options=["Semua", "1", "2", "3", "4"], index=0)
    with col_cari3:
        if 'KOD KAWASAN' in df_pusat.columns and 'DAERAH' in df_pusat.columns:
            df_daerah = df_pusat[['KOD KAWASAN', 'DAERAH']].drop_duplicates().dropna().sort_values('DAERAH')
            senarai_daerah = {'Semua': 'Semua'}
            senarai_daerah.update(dict(zip(df_daerah['DAERAH'], df_daerah['KOD KAWASAN'])))
        else: senarai_daerah = {'Semua': 'Semua'}
        pilihan_daerah_nama = st.selectbox("3. Pilih Daerah", options=list(senarai_daerah.keys()), index=0)
        pilihan_daerah_kod = senarai_daerah[pilihan_daerah_nama]
    if carian_mp:
        mask_kod = df_full['KOD MATA PELAJARAN'].astype(str).str.contains(carian_mp, case=False, na=False)
        hasil_mp = df_full[mask_kod]
        if pilihan_kertas != "Semua" and 'KERTAS' in hasil_mp.columns: hasil_mp = hasil_mp[hasil_mp['KERTAS'].astype(str).str.contains(pilihan_kertas, case=False, na=False)]
        if pilihan_daerah_kod != "Semua" and 'KOD KAWASAN' in hasil_mp.columns: hasil_mp = hasil_mp[hasil_mp['KOD KAWASAN'] == pilihan_daerah_kod]
        if not hasil_mp.empty:
            teks_daerah = "" if pilihan_daerah_nama == "Semua" else f" di {pilihan_daerah_nama}"
            st.success(f"✅ Dijumpai **{hasil_mp['NO PUSAT'].nunique()} pusat** untuk Kod **{carian_mp}** Kertas **{pilihan_kertas}**{teks_daerah}")
            nama_sekolah_col = 'NAMA SEKOLAH' if 'NAMA SEKOLAH' in hasil_mp.columns else 'NAMA PUSAT'
            masa_col = 'MASA MENJAWAB' if 'MASA MENJAWAB' in hasil_mp.columns else 'MASA'
            cols_untuk_papar = ['TARIKH', masa_col, 'NO PUSAT', nama_sekolah_col, 'DAERAH']
            cols_untuk_papar = [c for c in cols_untuk_papar if c in hasil_mp.columns]
            def highlight_past(row):
                hari_ini = pd.Timestamp.now().normalize()
                if 'TARIKH' in row and pd.notna(row['TARIKH']):
                    if row['TARIKH'].normalize() < hari_ini: return ['background-color: #FFCDD2'] * len(row)
                return [''] * len(row)
            st.dataframe(hasil_mp[cols_untuk_papar].style.apply(highlight_past, axis=1), use_container_width=True, hide_index=True)
        else: st.warning(f"❌ Tiada data untuk Kod '{carian_mp}' Kertas {pilihan_kertas}")
    else: st.info("Sila masukkan Kod Mata Pelajaran untuk mula mencari")

with tab5:
    st.subheader("Analisis Ringkas")
    if 'DAERAH' in df_pusat.columns: st.bar_chart(df_pusat['DAERAH'].value_counts())

# TAB BARU UNTUK EDIT
with tab6:
    st.subheader("✏️ Edit Data Excel")
    st.warning("⚠️ Perubahan di sini TIDAK auto save ke Github. Kena download dan upload manual balik.")
    
    pilihan_file = st.selectbox("Pilih file yang nak edit", ["nama sekolah.xlsx", "senarai pusat.xlsx", "senarai bilik kebal.xls", "JADUAL PEPERISAAN SPM 2026.xlsx"])
    
    if pilihan_file == "nama sekolah.xlsx": df_edit = df_nama.copy()
    elif pilihan_file == "senarai pusat.xlsx": df_edit = df_pusat.copy()
    elif pilihan_file == "senarai bilik kebal.xls": df_edit = df_bilik.copy()
    else: df_edit = df_jadual.copy()
    
    st.info("Boleh klik terus dalam table untuk edit. Lepas edit tekan Download.")
    edited_df = st.data_editor(df_edit, use_container_width=True, num_rows="dynamic")
    
    # BUTTON DOWNLOAD FILE YANG DAH EDIT
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        edited_df.to_excel(writer, index=False, sheet_name='Sheet1')
    st.download_button(
        label="📥 Download File Yang Dah Edit",
        data=output.getvalue(),
        file_name=f"EDITED_{pilihan_file}",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.caption("Lepas download, upload file `EDITED_...` ni ke Github untuk gantikan file lama.")

st.write("---")
st.caption("akashah ismail")
