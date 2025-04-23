import pandas as pd
import mlflow
import mlflow.catboost
from catboost import CatBoostRegressor
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        params = {
            "iterations": 100,
            "learning_rate": 0.1,
            "depth": 6
        }
        model = CatBoostRegressor(verbose=0)
        model.fit(X, y)

        y_pred = model.predict(X_val)
        rmse = mean_squared_error(y_val, y_pred)
        mae = mean_absolute_error(y_val, y_pred)
        r2 = r2_score(y_val, y_pred)

        # Логирование
        for key, value in params.items():
            mlflow.log_param(key, value)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # Логирование модели
        mlflow.catboost.log_model(model, "catboost-model", registered_model_name="fare_prediction_model")

if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "./data/silver"
    main(data_dir)
