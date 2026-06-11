from pyspark.sql import SparkSession

from pyspark.sql.functions import *

from pyspark.sql.types import IntegerType



MYSQL_URL = "jdbc:mysql://localhost:3306/bigdata_db?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai"



MYSQL_PROPERTIES = {

    "user": "root",

    "password": "614488", 

    "driver": "com.mysql.cj.jdbc.Driver"

}



spark = (
    SparkSession.builder
    .appName("ZhihuUserAnalysis")
    .config(
        "spark.jars",
        "/opt/zuel_bigdata/jars/mysql-connector-java-8.0.26.jar"
    )
    .getOrCreate()
)



print("开始读取数据...")



df = spark.read.jdbc(

    url=MYSQL_URL,

    table="user_raw_data",

    properties=MYSQL_PROPERTIES

)



print("总记录数:", df.count())



df = df.select(

    col("name"),

    col("gender").cast(IntegerType()).alias("gender"),

    col("answer_count").cast(IntegerType()).alias("answer_count"),

    col("articles_count").cast(IntegerType()).alias("articles_count")

)



# ==================

# 性别统计

# ==================



gender_df = df.withColumn(

    "gender_label",

    when(col("gender") == 1, "男")

    .when(col("gender") == 0, "女")

    .otherwise("未知")

)



gender_result = gender_df.groupBy(

    "gender_label"

).count()



gender_result.write.mode("overwrite").jdbc(

    MYSQL_URL,

    "res_gender_dist",

    properties=MYSQL_PROPERTIES

)



# ==================

# 回答数统计

# ==================



answer_result = df.withColumn(

    "answer_range",

    when(col("answer_count") == 0, "0")

    .when(col("answer_count") <= 100, "1-100")

    .when(col("answer_count") <= 500, "101-500")

    .when(col("answer_count") <= 1000, "501-1000")

    .otherwise("1000+")

)



answer_result = answer_result.groupBy(

    "answer_range"

).count()



answer_result.write.mode("overwrite").jdbc(

    MYSQL_URL,

    "res_answer_dist",

    properties=MYSQL_PROPERTIES

)



# ==================

# 发文统计

# ==================



post_result = df.withColumn(

    "post_range",

    when(col("articles_count") == 0, "0")

    .when(col("articles_count") <= 10, "1-10")

    .when(col("articles_count") <= 50, "11-50")

    .when(col("articles_count") <= 100, "51-100")

    .otherwise("100+")

)



post_result = post_result.groupBy(

    "post_range"

).count()



post_result.write.mode("overwrite").jdbc(

    MYSQL_URL,

    "res_post_dist",

    properties=MYSQL_PROPERTIES

)



# ==================

# 姓氏统计 

# ==================



surname_df = df.filter(

    length(col("name")) >= 2

)



surname_df = surname_df.withColumn(

    "surname",

    substring(col("name"), 1, 1)

)



# 仅保留中文



surname_df = surname_df.filter(

    col("surname").rlike("^[\\u4e00-\\u9fa5]$")

)



# 过滤昵称前缀



bad_words = [

    "小",

    "大",

    "阿",

    "我",

    "一",

    "这",

    "那",

    "某"

]



surname_df = surname_df.filter(

    ~col("surname").isin(bad_words)

)



surname_result = surname_df.groupBy(

    "surname"

).count()



surname_result = surname_result.withColumnRenamed(

    "count",

    "cnt"

)



surname_result.write.mode("overwrite").jdbc(

    MYSQL_URL,

    "res_surname_dist",

    properties=MYSQL_PROPERTIES

)



top10 = surname_result.orderBy(

    desc("cnt")

).limit(10)



top10.write.mode("overwrite").jdbc(

    MYSQL_URL,

    "res_surname_top10",

    properties=MYSQL_PROPERTIES

)





print("分析完成")



spark.stop()
