# CRM SITUM App

Questa è una Web App sviluppata con **Streamlit** per supportare il monitoraggio delle interazioni nel progetto SITUM.

## Funzionalità
- Dashboard personalizzate per ciascun SITUM-Angel
- Registrazione interazioni con imprese, docenti e studenti
- Visualizzazione degli obiettivi e progresso verso eventi chiave
- Caricamento e visualizzazione di vecchie liste (rubrica)
- Grafici riepilogativi per il coordinatore

## Installazione

1. Clona il repository o scarica il pacchetto .zip
2. Installa i requisiti:

```bash
pip install -r requirements.txt
```

3. Avvia l'app:

```bash
streamlit run crm_situm_app.py
```

## Configurazione Dominio

Per pubblicare su un dominio personalizzato (es. situm.org), puoi usare:
- Streamlit Cloud
- Render.com
- Server personale con nginx + gunicorn

## File

- `crm_situm_app.py`: Codice principale dell'app
- `interazioni_log.csv`: Database delle interazioni
- `requirements.txt`: Dipendenze Python
- `README.md`: Istruzioni
