# 📚 Book Review Backend – Flask + MongoDB

Questo progetto è un microservizio backend scritto in Flask per la gestione utenti e la valutazione di libri, con persistenza su MongoDB.

## 📦 Requisiti

- Docker + Docker Compose
- Python 3.10+ (se vuoi eseguire localmente senza Docker)
- MongoDB

## ▶️ Avvio con Docker

1. **Crea un file `.env` (opzionale)** oppure imposta le variabili nel tuo sistema:

```env
MONGO_URI=mongodb://root:example@mongo:27017/login_db?authSource=admin
FLASK_ENV=development
