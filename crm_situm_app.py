
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="SITUM CRM", layout="wide")

LOG_FILE = "interazioni_log.csv"
OBJ_FILE = "obiettivi.csv"

# Inizializza i file se non esistono
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "data", "nome", "target", "affiliazione", "regione", "evento",
        "stato_interazione", "fonte", "note", "telefono", "trascrizione", "angel"
    ]).to_csv(LOG_FILE, index=False)

if not os.path.exists(OBJ_FILE):
    pd.DataFrame(columns=["angel", "target", "evento", "obiettivo", "deadline"]).to_csv(OBJ_FILE, index=False)

df_log = pd.read_csv(LOG_FILE)
df_obj = pd.read_csv(OBJ_FILE)

angel = st.sidebar.selectbox("SITUM-Angel in uso", [
    "Nicole", "Nadia", "Alberto", "Bianca", "Vanessa", "Giorgio", "Alessandro (Coordinatore)"
])

# 🔧 Funzioni di supporto
def get_val(target, angel, evento):
    match = df_obj[(df_obj["angel"] == angel) & (df_obj["target"] == target) & (df_obj["evento"] == evento)]
    return match["obiettivo"].values[0] if not match.empty else 0

def get_deadline(angel, evento):
    match = df_obj[(df_obj["angel"] == angel) & (df_obj["evento"] == evento)]
    return match["deadline"].values[0] if not match.empty else pd.Timestamp.today()

def aggiorna_obiettivi(angel, evento, imp, doc, stu, deadline):
    nuovi = pd.DataFrame([
        {"angel": angel, "target": "Impresa", "evento": evento, "obiettivo": imp, "deadline": deadline},
        {"angel": angel, "target": "Docente", "evento": evento, "obiettivo": doc, "deadline": deadline},
        {"angel": angel, "target": "Studente", "evento": evento, "obiettivo": stu, "deadline": deadline}
    ])
    df_existing = df_obj[~((df_obj["angel"] == angel) & (df_obj["evento"] == evento))]
    updated = pd.concat([df_existing, nuovi], ignore_index=True)
    updated.to_csv(OBJ_FILE, index=False)

def conta_raggiunti(df, angel, evento):
    filtro = (df["angel"] == angel) & (df["evento"] == evento) & (df["stato_interazione"] == "Pagato")
    return df[filtro].groupby("target").size().to_dict()

def mostra_obiettivi_e_piano(angel):
    st.subheader("🎯 Obiettivi e Suggerimenti Operativi")
    eventi_esistenti = df_obj[df_obj["angel"] == angel]["evento"].unique().tolist()
    evento = st.selectbox("Seleziona o scrivi evento", ["SITUM-FUTURE", "SITUM-PLAY", "SUMMER SCHOOL"] + list(set(eventi_esistenti) - {"SITUM-FUTURE", "SITUM-PLAY", "SUMMER SCHOOL"}), index=0)

    with st.form("modifica_obiettivi"):
        st.markdown("#### 📅 Imposta Obiettivi e Deadline")
        col1, col2, col3, col4 = st.columns(4)
        ob_impresa = col1.number_input("🏢 Imprese", min_value=0, value=int(get_val("Impresa", angel, evento)))
        ob_docente = col2.number_input("🎓 Docenti", min_value=0, value=int(get_val("Docente", angel, evento)))
        ob_studente = col3.number_input("🧑‍🎓 Studenti", min_value=0, value=int(get_val("Studente", angel, evento)))
        deadline = col4.date_input("📅 Deadline", value=pd.to_datetime(get_deadline(angel, evento)))
        salva = st.form_submit_button("💾 Salva")
        if salva:
            aggiorna_obiettivi(angel, evento, ob_impresa, ob_docente, ob_studente, deadline)
            st.success("Obiettivi aggiornati!")

    st.markdown("### 📊 Stato Avanzamento & Suggerimenti")
    raggiunti = conta_raggiunti(df_log, angel, evento)
    deadline_dt = pd.to_datetime(get_deadline(angel, evento))
    giorni_mancanti = max((deadline_dt - pd.Timestamp.today()).days, 1)

    for target, emoji, obiettivo in [
        ("Impresa", "🏢", ob_impresa),
        ("Docente", "🎓", ob_docente),
        ("Studente", "🧑‍🎓", ob_studente)
    ]:
        raggiunto = raggiunti.get(target, 0)
        progresso = int((raggiunto / obiettivo) * 100) if obiettivo else 0
        suggeriti = int(round((obiettivo - raggiunto) * 2 / giorni_mancanti)) if obiettivo > raggiunto else 0
        st.markdown(f"**{emoji} {target}s**")
        st.metric("🎯 Obiettivo", obiettivo)
        st.metric("✅ Raggiunti", raggiunto)
        st.metric("📈 Avanzamento", f"{progresso}%")
        st.metric("🧠 Da contattare al giorno", suggeriti)
        st.progress(progresso / 100)


def registra_interazione():
    st.subheader("➕ Registra nuova interazione")
    with st.form("nuova_interazione"):
        col1, col2 = st.columns(2)

        nome = col1.text_input("Nome")
        target = col2.selectbox("Target", ["Impresa", "Docente", "Studente"])
        affiliazione = col1.text_input("Affiliazione")
        regione = col2.selectbox("Regione", ["Marche", "Umbria", "Abruzzo"])
        evento = col1.selectbox("Evento", ["SITUM-FUTURE", "SITUM-PLAY", "SUMMER SCHOOL"])
        stato = col2.selectbox("Stato Interazione", [
            "Contattato", 
            "Lettera firmata", 
            "Form compilato", 
            "Pagato"
        ])
        fonte = col1.selectbox("Fonte", ["Email", "Telefono", "Instagram", "Sito", "Altro"])
        telefono = col2.text_input("Telefono")
        note = st.text_area("Note")
        trascrizione = st.text_area("Trascrizione (se presente)")

        allegato_email = st.file_uploader("📧 Allega email inviata (facoltativa)", type=["eml", "pdf", "txt"])
        screenshot_msg = st.file_uploader("💬 Screenshot o messaggio (facoltativo)", type=["txt", "png", "jpg", "jpeg"])

        salva = st.form_submit_button("💾 Salva")
        if salva:
            nuova = pd.DataFrame([{
                "data": datetime.today().strftime("%Y-%m-%d"),
                "nome": nome,
                "target": target,
                "affiliazione": affiliazione,
                "regione": regione,
                "evento": evento,
                "stato_interazione": stato,
                "fonte": fonte,
                "note": note,
                "telefono": telefono,
                "trascrizione": trascrizione,
                "angel": angel
            }])
            pd.concat([df_log, nuova], ignore_index=True).to_csv(LOG_FILE, index=False)
            st.success("Interazione salvata con successo!")
def cancella_interazione(angel):
    st.subheader("🗑️ Cancella Interazioni")
    df_mie = df_log[df_log["angel"] == angel].copy()
    df_mie = df_mie.sort_values(by="data", ascending=False).reset_index()

    if df_mie.empty:
        st.info("Nessuna interazione da mostrare.")
        return

    df_mie["riga"] = df_mie.index
    selezionata = st.selectbox("Seleziona interazione da cancellare", df_mie.apply(
        lambda row: f"{row['data']} - {row['nome']} ({row['target']}, {row['evento']})", axis=1
    ))

    if st.button("❌ Cancella questa interazione"):
        idx = df_mie[df_mie.apply(
            lambda row: f"{row['data']} - {row['nome']} ({row['target']}, {row['evento']})", axis=1
        ) == selezionata]["index"].values[0]

        df_nuovo = df_log.drop(index=idx).reset_index(drop=True)
        df_nuovo.to_csv(LOG_FILE, index=False)
        st.success("Interazione cancellata con successo. Ricaricare la pagina per aggiornare.")


def mostra_rubrica_contatti(angel):
    st.subheader("📇 Rubrica Contatti")
    df_rubrica = df_log.copy() if angel == "Alessandro (Coordinatore)" else df_log[df_log["angel"] == angel]

    col1, col2, col3 = st.columns(3)
    evento_filtro = col1.selectbox("Evento", ["Tutti"] + sorted(df_rubrica["evento"].dropna().unique()))
    target_filtro = col2.selectbox("Target", ["Tutti", "Impresa", "Docente", "Studente"])
    stato_filtro = col3.selectbox("Stato", ["Tutti"] + sorted(df_rubrica["stato_interazione"].dropna().unique()))

    if evento_filtro != "Tutti":
        df_rubrica = df_rubrica[df_rubrica["evento"] == evento_filtro]
    if target_filtro != "Tutti":
        df_rubrica = df_rubrica[df_rubrica["target"] == target_filtro]
    if stato_filtro != "Tutti":
        df_rubrica = df_rubrica[df_rubrica["stato_interazione"] == stato_filtro]

    st.dataframe(df_rubrica.sort_values(by="data", ascending=False), use_container_width=True)
    csv = df_rubrica.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Esporta Rubrica in CSV", data=csv, file_name=f"rubrica_{angel}.csv", mime="text/csv")

# UI principale
if angel == "Alessandro (Coordinatore)":
    import plotly.graph_objects as go

    st.title("🧭 Dashboard Coordinatore")

    evento_selezionato = st.selectbox("📅 Seleziona evento", sorted(df_log["evento"].dropna().unique()))
    df_evento = df_log[df_log["evento"] == evento_selezionato].copy()
    df_evento["data"] = pd.to_datetime(df_evento["data"])
    df_evento = df_evento[df_evento["angel"].isin(["Nicole", "Alberto", "Vanessa"])]
    df_evento["giorno"] = df_evento["data"].dt.date

    colori = {
        ("Nicole", "Impresa"): "red",
        ("Nicole", "Docente"): "blue",
        ("Nicole", "Studente"): "green",
        ("Alberto", "Impresa"): "purple",
        ("Alberto", "Docente"): "orange",
        ("Alberto", "Studente"): "pink",
        ("Vanessa", "Impresa"): "black",
        ("Vanessa", "Docente"): "yellow",
        ("Vanessa", "Studente"): "aqua",
    }

    fig = go.Figure()

    for angel_sel in ["Nicole", "Alberto", "Vanessa"]:
        for target in ["Impresa", "Docente", "Studente"]:
            df_sub = df_evento[
                (df_evento["angel"] == angel_sel) &
                (df_evento["target"] == target) &
                (df_evento["stato_interazione"].isin(["Lettera firmata", "Pagato"]))
            ].groupby("giorno").size().reset_index(name="interazioni")

            if not df_sub.empty:
                df_sub["cumulativo"] = df_sub["interazioni"].cumsum()
                fig.add_trace(go.Scatter(
                    x=df_sub["giorno"],
                    y=df_sub["cumulativo"],
                    mode='lines+markers',
                    name=f"{angel_sel} - {target}",
                    line=dict(color=colori.get((angel_sel, target), "gray"))
                ))

    fig.update_layout(title=f"📈 Partecipanti Cumulativi per Angel - Evento: {evento_selezionato}",
                      xaxis_title="Data",
                      yaxis_title="Partecipanti cumulativi",
                      legend_title="Angel - Target")

    st.plotly_chart(fig, use_container_width=True)

    mostra_rubrica_contatti(angel)
else:
    st.title(f"👤 Dashboard di {angel}")
    mostra_obiettivi_e_piano(angel)
    registra_interazione()
    mostra_rubrica_contatti(angel)
    cancella_interazione(angel)

