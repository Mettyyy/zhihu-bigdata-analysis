from flask import Flask, render_template
import pymysql
import pandas as pd

app = Flask(__name__)

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "614488",
    "database": "bigdata_db",
    "charset": "utf8mb4"
}


def get_conn():
    return pymysql.connect(**MYSQL_CONFIG)


# ==========================
# 首页
# ==========================
@app.route("/")
def index():

    conn = get_conn()

    # 读取性别分布
    gender_df = pd.read_sql(
        "SELECT * FROM res_gender_dist",
        conn
    )

    # 读取回答数分布
    answer_df = pd.read_sql(
        "SELECT * FROM res_answer_dist",
        conn
    )

    # 读取发文数分布
    post_df = pd.read_sql(
        "SELECT * FROM res_post_dist",
        conn
    )

    # 读取总用户数
    total_user = pd.read_sql(
        "SELECT COUNT(*) total FROM user_raw_data",
        conn
    ).iloc[0]["total"]

    # 新增：直接从数据库读取姓氏词云数据
    surname_df = pd.read_sql(
        "SELECT surname, cnt FROM res_surname_dist",
        conn
    )

    # ==========================
    # 回答数固定排序
    # ==========================
    answer_order = [
        "0",
        "1-100",
        "101-500",
        "501-1000",
        "1000+"
    ]

    answer_df["answer_range"] = pd.Categorical(
        answer_df["answer_range"],
        categories=answer_order,
        ordered=True
    )

    answer_df = answer_df.sort_values(
        "answer_range"
    )

    # ==========================
    # 发文数固定排序
    # ==========================
    post_order = [
        "0",
        "1-10",
        "11-50",
        "51-100",
        "100+"
    ]

    post_df["post_range"] = pd.Categorical(
        post_df["post_range"],
        categories=post_order,
        ordered=True
    )

    post_df = post_df.sort_values(
        "post_range"
    )

    conn.close()

    # 转换性别数据格式
    gender_data = [
        {
            "name": str(r["gender_label"]),
            "value": int(r["count"])
        }
        for _, r in gender_df.iterrows()
    ]

    # 新增：转换姓氏词云数据格式，直接对接 ECharts Wordcloud
    surname_data = [
        {
            "name": str(r["surname"]),
            "value": int(r["cnt"])
        }
        for _, r in surname_df.iterrows()
    ]

    return render_template(
        "index.html",

        total_user=int(total_user),

        gender_data=gender_data,

        answer_x=answer_df["answer_range"].tolist(),
        answer_y=answer_df["count"].tolist(),

        post_x=post_df["post_range"].tolist(),
        post_y=post_df["count"].tolist(),

        # 将词云数据传给前端
        surname_data=surname_data
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
