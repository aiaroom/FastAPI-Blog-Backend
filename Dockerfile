# Многоступенчатая сборка для оптимизации размера образа
FROM python:3.11-slim AS builder

# Устанавливаем зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-slim

# Создаем непривилегированного пользователя для безопасности
RUN useradd -m -u 1000 appuser
USER appuser

WORKDIR /app

# Копируем зависимости из билдера
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код приложения
COPY --chown=appuser:appuser . .

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Экспонируем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]