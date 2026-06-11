# Zhihu User Portrait Analysis System

## Technology Stack

- Python
- PySpark
- MySQL
- Flask
- ECharts
- WordCloud

## Project Structure

zuel_bigdata/
├── jars/
├── pyspark/
├── sql/
├── web/
└── README.md

## Run

### 1. Create Database

mysql -uroot -p < sql/create_database.sql

### 2. Run Spark Analysis

spark-submit \
--jars jars/mysql-connector-java-8.0.26.jar \
pyspark/spark_analysis.py

### 3. Run Flask

cd web

python3 app.py

Visit:

http://服务器IP:5000
