import pandas as pd
import mlflow
import mlflow.catboost
from catboost import CatBoostRegressor
import joblib
import os

def main(data_dir):
    mlflow.set_tracking_uri("file:/app/mlflow")
    # Загрузка данных
    data = pd.read_parquet(data_dir)  # пример
    print("Columns in dataset:", data.columns.tolist())
    print("First few rows:\n", data.head())
    
    X = data.drop('Historical_Cost_of_Ride', axis=1)
    y = data['Historical_Cost_of_Ride']

    # Инициализация MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")  # если ты в Docker
    mlflow.set_experiment("price-predict-experiment")

    with mlflow.start_run():
        model = CatBoostRegressor(verbose=0)
        model.fit(X, y)

        # Логирование модели
        mlflow.catboost.log_model(model, "catboost-model")

if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "./data/silver"
    main(data_dir)
