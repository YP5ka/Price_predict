import joblib
import pandas as pd
import os
import yaml
import types
import sys

# 🔧 Шаг 1: определить функцию с тем же именем, что была при обучении
expected_columns = [
    'Number_of_Riders',
    'Number_of_Drivers',
    'Number_of_Past_Rides',
    'Average_Ratings',
    'Vehicle_Type',
    'Expected_Ride_Duration',
    'Time_of_Booking_Afternoon',
    'Time_of_Booking_Evening',
    'Time_of_Booking_Morning',
    'Time_of_Booking_Night',
    'Customer_Loyalty_Status_Gold',
    'Customer_Loyalty_Status_Regular',
    'Customer_Loyalty_Status_Silver',
    'Location_Category_Rural',
    'Location_Category_Suburban',
    'Location_Category_Urban'
]
def preprocess_data(df):
    df = df.copy()

    # Сохраняем только нужные признаки
    df = df[['Number_of_Riders', 'Number_of_Drivers', 'Number_of_Past_Rides',
             'Average_Ratings', 'Vehicle_Type', 'Expected_Ride_Duration',
             'Time_of_Booking', 'Customer_Loyalty_Status', 'Location_Category']]

    # Кодируем Vehicle_Type
    df['Vehicle_Type'] = df['Vehicle_Type'].map({'Economy': 0, 'Premium': 1})

    # One-hot кодируем категориальные признаки
    df = pd.get_dummies(df, columns=[
        'Time_of_Booking', 'Customer_Loyalty_Status', 'Location_Category'
    ])

    # Добавляем недостающие признаки
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    # Упорядочиваем
    df = df[expected_columns]

    return df


# 🔧 Шаг 2: вручную "подсунуть" функцию в __main__
main_module = types.ModuleType("__main__")
main_module.preprocess_data = preprocess_data
sys.modules["__main__"] = main_module

# 🔧 Шаг 3: загрузка конфига и модели
with open(os.path.join(os.path.dirname(__file__), "config.yaml")) as f:
    config = yaml.safe_load(f)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'ride_cost_model.pkl')
MODEL_PATH = os.path.abspath(MODEL_PATH)

model = joblib.load(MODEL_PATH)


# 🔧 Шаг 4: функция предсказания
def predict(data: dict) -> float:
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return round(prediction, 2)
