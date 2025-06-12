# SITUM-Angels CRM

Questa è una Web App sviluppata con Streamlit per supportare il monitoraggio delle interazioni nel progetto SITUM.

## ✨ Funzionalità

- Dashboard personalizzate per ciascun SITUM-Angel
- Dashboard coordinatore generale (Alessandro) con riepilogo per regione e target
- Obiettivi configurabili per evento e target
- Gestione delle interazioni con 3 stati: Contattato, Ingegaggiato con firma, Ingegaggiato e pagato
- Caricamento di trascrizioni vocali o note testuali
- Caricamento di vecchie liste per ricontatto (rubrica)
- Grafici riepilogativi per confrontare stagioni
- Scadenze impostabili per ogni obiettivo
- Affiliazione (dipartimento/impresa/corso) e contatto telefonico
- Icone e interfaccia visuale migliorata

## 📁 File del progetto

- `crm_situm_app.py`: Codice principale dell'app
- `interazioni_log.csv`: Database delle interazioni in tempo reale
- `obiettivi.csv`: Obiettivi per angel, evento, target, con deadline
- `requirements.txt`: Dipendenze Python
- `README.md`: Istruzioni

## 🛠️ Installazione

```bash
pip install -r requirements.txt
streamlit run crm_situm_app.py
