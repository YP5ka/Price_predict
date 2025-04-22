FROM python:3.10

WORKDIR /app

COPY . .
COPY ./ml/train_model_mlflow.py /app/ml/train_model_mlflow.py
# Обновляем pip и ставим wheel и setuptools, чтобы не падала установка scipy, pillow и т.п.
RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]

