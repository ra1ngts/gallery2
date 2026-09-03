# =========================
# 1. Build Svelte
# =========================
FROM node:24-slim AS frontend
WORKDIR /app
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install
COPY frontend/ ./frontend/
COPY static/ ./static/
COPY main/ ./main/
RUN cd frontend && npm run build

# =========================
# 2. Django
# =========================
FROM python:3.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=frontend /app/main/static/svelte/assets ./main/static/svelte/assets
RUN SECRET_KEY=build-only-secret \
    DB_NAME=build \
    DB_USER=build \
    DB_PASSWORD=build \
    DB_HOST=localhost \
    DB_PORT=5432 \
    python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "gallery2.wsgi:application", "--bind", "0.0.0.0:8000"]
LABEL org.opencontainers.image.authors="david.khurts@gmail.com" \
      org.opencontainers.image.version="0.1" \
      org.opencontainers.image.description="gallery2"