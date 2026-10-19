FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY Audios ./Audios

ENV AUDIO_FOLDER_PATH=/app/Audios \
    PYTHONUNBUFFERED=1

# Sem root dentro do container
RUN useradd --create-home gritador
USER gritador

CMD ["python", "main.py"]
