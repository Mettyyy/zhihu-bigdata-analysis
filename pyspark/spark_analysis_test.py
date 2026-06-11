from pyspark.sql import SparkSession
from pyspark.sql.functions import col

MYSQL_URL = "jdbc:mysql://localhost:3306/bigdata_db?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai"

MYSQL_PROPERTIES = {
    "user": "bigdata",
    "password": "BigData123!",
    "driver": "com.mysql.cj.jdbc.Driver"
}

spark = SparkSession.builder \
    .appName("ZhihuUserAnalysis") \
    .config(
        "spark.jars",
        "/opt/zuel_bigdata/jars/mysql-connector-java-8.0.26.jar"
    ) \
    .getOrCreate()

print("开始读取数据...")

df = spark.read.jdbc(
    url=MYSQL_URL,
    table="user_raw_data",
    properties=MYSQL_PROPERTIES
)

print("总记录数：", df.count())

df.show(5)

spark.stop()
