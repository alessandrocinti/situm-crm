# SITUM-Angels CRM (Versione Unificata)

Questa Web App, sviluppata con Streamlit, supporta il monitoraggio personalizzato delle interazioni tra SITUM-Angels e target (Imprese, Docenti, Studenti) per gli eventi SITUM.

## Funzionalità
- Dashboard personalizzate per ciascun Angel (Nicole, Nadia, Alberto, Bianca, Vanessa, Giorgio)
- Dashboard coordinatore (Alessandro) con dati aggregati per regione ed evento
- Registrazione delle interazioni con campi completi:
  - Stato interazione (Contattato, Lettera firmata, Pagato)
  - Affiliazione (corso, azienda, dipartimento)
  - Fonte (email, telefono, sito, Instagram)
  - Note, Trascrizione, Telefono
- Caricamento delle trascrizioni e rubriche storiche
- Obiettivi configurabili per target ed evento con deadline
- Salvataggio persistente delle interazioni in `interazioni_log.csv`
- Grafici mensili di andamento per il coordinatore
- Compatibile con Streamlit Cloud e GitHub

## Installazione
```bash
pip install -r requirements.txt
streamlit run crm_situm_app_unificato.py
```

## File inclusi
- `crm_situm_app_unificato.py`: Codice dell'app
- `interazioni_log.csv`: Registro persistente delle interazioni
- `requirements.txt`: Dipendenze
