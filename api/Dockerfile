# Используем официальный образ Python
FROM python:3.10-slim

WORKDIR /app

# Скопировать и api/, и ml/, и data/, если надо
COPY ./api ./api
COPY ./ml ./ml
COPY ./data ./data

# Установить зависимости FastAPI + ML
COPY ./ml/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Или requirements.txt из api, если у тебя он там
# COPY ./api/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Убедиться, что Python видит и /app/ml
ENV PYTHONPATH=/app

# Открываем порт
EXPOSE 8000

# Запускаем FastAPI
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]