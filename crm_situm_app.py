import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_extras.colored_header import colored_header
import matplotlib.pyplot as plt

# --- CONFIGURAZIONE ---
ANGELS = ["Nicole", "Nadia", "Alberto", "Bianca", "Vanessa", "Giorgio", "Alessandro"]
REGIONI = {"Nicole": "Marche", "Nadia": "Marche", "Alberto": "Umbria", "Bianca": "Umbria", "Vanessa": "Abruzzo", "Giorgio": "Tutte", "Alessandro": "Tutte"}
EVENTI_DATE = {"SITUM-PLAY": "2025-07-05", "SITUM-FUTURE": "2025-07-10", "SUMMER SCHOOL": "2025-07-25"}

st.set_page_config(page_title="CRM SITUM", layout="wide")

# --- SELEZIONE UTENTE ---
st.sidebar.title("Accesso utente")
utente = st.sidebar.selectbox("Chi sei?", ANGELS)
territorio = REGIONI[utente]
is_admin = utente == "Giorgio"
is_coordinatore = utente == "Alessandro"

colored_header(f"Dashboard CRM - {utente}", description=f"Regione: {territorio if not (is_admin or is_coordinatore) else 'Tutte'}", color_name="violet-70")

# --- CARICAMENTO LOG ---
try:
    df_log = pd.read_csv("interazioni_log.csv")
except FileNotFoundError:
    df_log = pd.DataFrame(columns=["data", "tipo", "nome_contatto", "email", "telefono", "affiliazione", "angel", "fonte", "descrizione", "regione", "evento"])

# --- SELEZIONE EVENTO E DEADLINE ---
evento_corrente = st.selectbox("Evento di riferimento", ["SITUM-PLAY", "SITUM-FUTURE", "SUMMER SCHOOL"])
data_evento = st.date_input("Data evento", value=pd.to_datetime(EVENTI_DATE[evento_corrente]))
dealine = data_evento - timedelta(days=15)
st.caption(f"📅 Deadline obiettivi: {dealine.strftime('%d/%m/%Y')}")

# --- OBIETTIVI PER OGNI ANGEL ---
if not is_admin and not is_coordinatore:
    st.subheader("🎯 I tuoi obiettivi")
    col1, col2, col3 = st.columns(3)
    target_imprese = col1.number_input("🏢 Obiettivo Imprese", min_value=0, max_value=50, value=15, key="imp")
    target_docenti = col2.number_input("🎓 Obiettivo Docenti", min_value=0, max_value=50, value=15, key="doc")
    target_studenti = col3.number_input("🧑‍🎓 Obiettivo Studenti", min_value=0, max_value=300, value=30, key="stu")

    df_log_filtered = df_log[(df_log["angel"] == utente) & (df_log["evento"] == evento_corrente)]
    col1.metric("🏢 Imprese", len(df_log_filtered[df_log_filtered["tipo"] == "Impresa"]), f"su {target_imprese}")
    col2.metric("🎓 Docenti", len(df_log_filtered[df_log_filtered["tipo"] == "Docente"]), f"su {target_docenti}")
    col3.metric("🧑‍🎓 Studenti", len(df_log_filtered[df_log_filtered["tipo"] == "Studente"]), f"su {target_studenti}")

# --- DASHBOARD COMPLETA PER COORDINATORE ---
if is_coordinatore:
    st.subheader("📋 Riepilogo per territorio, evento e target")
    for regione in ["Marche", "Umbria", "Abruzzo"]:
        st.markdown(f"### 📍 {regione}")
        df_reg = df_log[df_log["regione"] == regione]
        for evento in ["SITUM-PLAY", "SITUM-FUTURE", "SUMMER SCHOOL"]:
            st.markdown(f"**Evento: {evento}**")
            df_evento = df_reg[df_reg["evento"] == evento]
            col1, col2, col3 = st.columns(3)
            col1.metric("🏢 Imprese", len(df_evento[df_evento["tipo"] == "Impresa"]))
            col2.metric("🎓 Docenti", len(df_evento[df_evento["tipo"] == "Docente"]))
            col3.metric("🧑‍🎓 Studenti", len(df_evento[df_evento["tipo"] == "Studente"]))

    st.subheader("📊 Andamento storico per evento")
    agg = df_log.groupby(["evento", "tipo"]).size().unstack(fill_value=0)
    st.bar_chart(agg)

# --- REGISTRAZIONE INTERAZIONI ---
st.subheader("➕ Registra nuova interazione")
tipo = st.selectbox("Tipo di contatto", ["Studente", "Impresa", "Docente", "Amministrazione"])
nome_contatto = st.text_input("Nome del contatto")
email_contatto = st.text_input("Email del contatto")
telefono_contatto = st.text_input("Numero di telefono (facoltativo)")
affiliazione = st.text_input("Affiliazione (dipartimento, azienda o corso di studi)")
fonte = st.selectbox("Fonte dell'interazione", ["Telefono", "Email", "Sito web", "Instagram", "Incontro diretto", "Altro"])
data_interazione = st.date_input("Data dell'interazione", value=datetime.today())
descrizione = st.text_area("Descrizione dell'interazione")
regione = st.selectbox("Regione dell'interazione", ["Marche", "Umbria", "Abruzzo"]) if is_admin or is_coordinatore else territorio

# Upload trascrizione opzionale
with st.expander("📎 Aggiungi trascrizione da file (facoltativo)"):
    trascrizione_file = st.file_uploader("Carica un file .txt con la trascrizione della call", type="txt")
    trascrizione_testo = ""
    if trascrizione_file:
        trascrizione_testo = trascrizione_file.read().decode("utf-8")
        st.text_area("Contenuto trascrizione", trascrizione_testo, height=150)

# Salvataggio
if st.button("Registra interazione"):
    nuova_riga = pd.DataFrame({
        "data": [data_interazione],
        "tipo": [tipo],
        "nome_contatto": [nome_contatto],
        "email": [email_contatto],
        "telefono": [telefono_contatto],
        "affiliazione": [affiliazione],
        "angel": [utente],
        "fonte": [fonte],
        "descrizione": [descrizione],
        "regione": [regione],
        "evento": [evento_corrente]
    })
    df_log = pd.concat([df_log, nuova_riga], ignore_index=True)
    df_log.to_csv("interazioni_log.csv", index=False)
    st.success("Interazione registrata correttamente.")

# --- CARICAMENTO VECCHIE LISTE ---
with st.expander("📂 Caricamento o aggiornamento delle liste contatti"):
    studenti_file = st.file_uploader("Carica elenco studenti", type="csv")
    imprese_file = st.file_uploader("Carica elenco imprese", type="csv")
    docenti_file = st.file_uploader("Carica elenco docenti", type="csv")
    if studenti_file:
        df_studenti = pd.read_csv(studenti_file)
        st.success(f"Caricati {len(df_studenti)} studenti")
        st.dataframe(df_studenti)
    if imprese_file:
        df_imprese = pd.read_csv(imprese_file)
        st.success(f"Caricate {len(df_imprese)} imprese")
        st.dataframe(df_imprese)
    if docenti_file:
        df_docenti = pd.read_csv(docenti_file)
        st.success(f"Caricati {len(df_docenti)} docenti")
        st.dataframe(df_docenti)
