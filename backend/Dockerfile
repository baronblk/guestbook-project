FROM python:3.11-slim

# System-Abhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY ./app /app/app
COPY ./wait-for-db.py /app/wait-for-db.py
COPY ./create_admin.py /app/create_admin.py

# Upload-Ordner und Logs-Ordner erstellen
RUN mkdir -p /app/uploads /app/logs

# Scripts ausführbar machen
RUN chmod +x /app/wait-for-db.py /app/create_admin.py

# Port freigeben
EXPOSE 8000

# Startup-Befehl
CMD ["sh", "-c", "python wait-for-db.py && python create_admin.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
