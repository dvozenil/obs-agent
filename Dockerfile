# syntax=docker/dockerfile:1
FROM python:3.13-slim
LABEL org.opencontainers.image.source=https://github.com/dvozenil/obs-agent


RUN useradd -M appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .


USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]