from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import pandas as pd

# 🔧 Список ожидаемых признаков из модели
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

def main():
    spark = SparkSession.builder.appName("BronzeToSilverCompatible").getOrCreate()

    # 1. Загружаем "сырые" данные
    df = spark.read.parquet("/opt/data/bronze")

    # 2. Очищаем
    df = df.dropna()
    df = df.filter(col("Number_of_Drivers") <= 60)

    # 3. Приводим Vehicle_Type к числу
    df = df.withColumn(
        "Vehicle_Type",
        when(col("Vehicle_Type") == "Economy", 0)
        .when(col("Vehicle_Type") == "Premium", 1)
        .otherwise(None)
    )

    # 4. Переводим в pandas
    pdf = df.toPandas()

    # 5. Оставляем нужные признаки
    pdf = pdf[[
        'Number_of_Riders', 'Number_of_Drivers', 'Number_of_Past_Rides',
        'Average_Ratings', 'Vehicle_Type', 'Expected_Ride_Duration',
        'Time_of_Booking', 'Customer_Loyalty_Status', 'Location_Category', 'Historical_Cost_of_Ride'
    ]]

    # 6. One-hot кодируем категориальные
    pdf = pd.get_dummies(pdf, columns=[
        'Time_of_Booking', 'Customer_Loyalty_Status', 'Location_Category'
    ])

    # 7. Добавляем недостающие признаки
    for column in expected_columns:
      if column not in pdf.columns:
          pdf[column] = 0

    # 8. Упорядочиваем
    pdf = pdf[expected_columns + ['Historical_Cost_of_Ride']]

    # 9. Сохраняем как Spark DataFrame в Silver
    spark_df = spark.createDataFrame(pdf)
    spark_df.write.mode("overwrite").parquet("/opt/data/silver")

    spark.stop()

if __name__ == "__main__":
    main()