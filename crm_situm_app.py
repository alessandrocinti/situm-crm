import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="SITUM-Angels CRM", layout="wide")

# File
LOG_FILE = "interazioni_log.csv"
OBJ_FILE = "obiettivi.csv"

# Inizializzazione file se non esiste
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "data", "nome", "target", "affiliazione", "regione", "evento",
        "stato_interazione", "note", "telefono", "angel"
    ]).to_csv(LOG_FILE, index=False)

if not os.path.exists(OBJ_FILE):
    pd.DataFrame(columns=[
        "angel", "target", "evento", "obiettivo", "deadline"
    ]).to_csv(OBJ_FILE, index=False)

# Caricamento dati
df_log = pd.read_csv(LOG_FILE)
df_obj = pd.read_csv(OBJ_FILE)

# Sidebar: login Angel
angel = st.sidebar.selectbox("Chi sta usando il CRM?", [
    "Nicole", "Nadia", "Alberto", "Bianca", "Vanessa", "Giorgio", "Alessandro (Coordinatore)"
])

st.sidebar.markdown("---")

# Funzione per inserire interazione
def registra_interazione():
    with st.form("nuova_interazione"):
        st.subheader("Registra nuova interazione")
        nome = st.text_input("Nome")
        target = st.selectbox("Target", ["Impresa", "Docente", "Studente"])
        affiliazione = st.text_input("Affiliazione")
        regione = st.selectbox("Regione", ["Marche", "Umbria", "Abruzzo"])
        evento = st.selectbox("Evento", ["SITUM-PLAY", "SITUM-FUTURE", "Summer School"])
        stato = st.selectbox("Stato Interazione", ["Contattato", "Lettera firmata", "Pagato"])
        telefono = st.text_input("Telefono (facoltativo)")
        note = st.text_area("Note")
        submitted = st.form_submit_button("Salva")
        if submitted:
            nuova_riga = pd.DataFrame([{
                "data": datetime.today().strftime("%Y-%m-%d"),
                "nome": nome,
                "target": target,
                "affiliazione": affiliazione,
                "regione": regione,
                "evento": evento,
                "stato_interazione": stato,
                "note": note,
                "telefono": telefono,
                "angel": angel
            }])
            df_log_updated = pd.concat([df_log, nuova_riga], ignore_index=True)
            df_log_updated.to_csv(LOG_FILE, index=False)
            st.success("Interazione registrata!")

# Funzione per inserire obiettivo
def imposta_obiettivo():
    with st.form("imposta_obiettivo"):
        st.subheader("Imposta un nuovo obiettivo")
        target = st.selectbox("Target", ["Impresa", "Docente", "Studente"])
        evento = st.selectbox("Evento", ["SITUM-PLAY", "SITUM-FUTURE", "Summer School"])
        obiettivo = st.number_input("Numero da raggiungere", min_value=1, step=1)
        deadline = st.date_input("Scadenza (15 giorni prima evento)")
        submitted = st.form_submit_button("Aggiungi obiettivo")
        if submitted:
            nuova_riga = pd.DataFrame([{
                "angel": angel,
                "target": target,
                "evento": evento,
                "obiettivo": obiettivo,
                "deadline": deadline
            }])
            df_obj_updated = pd.concat([df_obj, nuova_riga], ignore_index=True)
            df_obj_updated.to_csv(OBJ_FILE, index=False)
            st.success("Obiettivo salvato!")

# Rubrica storica
def carica_lista_storica():
    st.subheader("Carica lista storica (opzionale)")
    file = st.file_uploader("CSV storico con gli stessi campi", type="csv")
    if file:
        df_storico = pd.read_csv(file)
        st.dataframe(df_storico)
        st.markdown("Puoi usarla per ricontattare vecchi contatti.")

# Dashboard
def mostra_dashboard():
    st.header(f"Dashboard per {angel}")
    col1, col2, col3 = st.columns(3)
    for i, target in enumerate(["Impresa", "Docente", "Studente"]):
        col = [col1, col2, col3][i]
        count = df_log[(df_log["angel"] == angel) & (df_log["target"] == target)].shape[0]
        col.metric(f"{target}s gestiti", count)

    st.subheader("Progresso obiettivi")
    df_obj_angel = df_obj[df_obj["angel"] == angel]
    if not df_obj_angel.empty:
        for evento in df_obj_angel["evento"].unique():
            st.markdown(f"### Evento: {evento}")
            df_evento = df_obj_angel[df_obj_angel["evento"] == evento]
            for _, row in df_evento.iterrows():
                raggiunti = df_log[
                    (df_log["angel"] == angel) &
                    (df_log["target"] == row["target"]) &
                    (df_log["evento"] == evento)
                ].shape[0]
                st.progress(min(raggiunti / row["obiettivo"], 1.0))
                st.write(f"**{row['target']}**: {raggiunti}/{row['obiettivo']} entro il {row['deadline']}")

# Dashboard coordinatore
def dashboard_coordinatore():
    st.title("📊 Dashboard Coordinatore Generale")
    for regione in df_log["regione"].unique():
        st.subheader(f"Regione: {regione}")
        col1, col2, col3 = st.columns(3)
        for i, target in enumerate(["Impresa", "Docente", "Studente"]):
            col = [col1, col2, col3][i]
            count = df_log[(df_log["regione"] == regione) & (df_log["target"] == target)].shape[0]
            col.metric(f"{target}s", count)

    # Grafico storico semplice
    st.subheader("📈 Andamento per mese")
    df_log["mese"] = pd.to_datetime(df_log["data"]).dt.to_period("M").astype(str)
    fig = px.bar(df_log.groupby(["mese", "target"]).size().reset_index(name="interazioni"),
                 x="mese", y="interazioni", color="target", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Interfaccia
if angel == "Alessandro (Coordinatore)":
    dashboard_coordinatore()
    with st.expander("Rubrica vecchie liste"):
        carica_lista_storica()
else:
    mostra_dashboard()
    registra_interazione()
    imposta_obiettivo()
    with st.expander("Rubrica vecchie liste"):
        carica_lista_storica()
