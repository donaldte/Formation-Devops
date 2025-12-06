FROM python:3.11-slim

WORKDIR /app

# Copier requirements depuis la racine
COPY ../../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier le code du service
COPY ./app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
