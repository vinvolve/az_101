# Databricks notebook source
# MAGIC %md
# MAGIC # Sample ETL Notebook
# MAGIC This is a placeholder for your data engineering logic.

# COMMAND ----------

dbutils.widgets.text("input_path", "dbfs:/mnt/bronze/data.csv")
input_path = dbutils.widgets.get("input_path")

print(f"Reading data from {input_path}")
# df = spark.read.csv(input_path, header=True)
# df.write.format("delta").mode("overwrite").save("dbfs:/mnt/silver/processed_data")
