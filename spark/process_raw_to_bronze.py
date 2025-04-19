from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName("RawToBronze").getOrCreate()

    # Пример: читаем данные
    df_raw = spark.read.csv("/opt/data/raw/dynamic_pricing.csv", header=True, inferSchema=True)

    # Простейшая обработка (например, убрать пустые значения)
    df_cleaned = df_raw.dropna()

    # Сохраняем в bronze слой
    df_cleaned.write.mode("overwrite").parquet("/opt/data/bronze")

    spark.stop()

if __name__ == "__main__":
    main()