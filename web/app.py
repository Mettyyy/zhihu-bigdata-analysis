from flask import Flask, render_template_string
import pymysql
import pandas as pd
from wordcloud import WordCloud

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
# 词云
# ==========================
def build_wordcloud(conn):

    df = pd.read_sql("SELECT surname, cnt FROM res_surname_dist", conn)

    words = {str(r["surname"]): int(r["cnt"]) for _, r in df.iterrows()}

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        font_path="/usr/share/fonts/wqy-microhei/wqy-microhei.ttc"
    )

    wc.generate_from_frequencies(words)
    wc.to_file("static/surname_wordcloud.png")

# ==========================
# ⭐直接使用数据库分组（关键修复）
# ==========================
def get_answer_data(conn):
    df = pd.read_sql("select * from res_answer_dist", conn)
    df = df.sort_values("answer_range")
    return df["answer_range"].tolist(), df["count"].tolist()

def get_post_data(conn):
    df = pd.read_sql("select * from res_post_dist", conn)
    df = df.sort_values("post_range")
    return df["post_range"].tolist(), df["count"].tolist()

# ==========================
# 首页
# ==========================
@app.route("/")
def index():

    conn = get_conn()

    gender_df = pd.read_sql("select * from res_gender_dist", conn)

    answer_x, answer_y = get_answer_data(conn)
    post_x, post_y = get_post_data(conn)

    total_user = pd.read_sql(
        "select count(*) total from user_raw_data",
        conn
    ).iloc[0]["total"]

    build_wordcloud(conn)
    conn.close()

    gender_data = [
        {"name": str(r["gender_label"]), "value": int(r["count"])}
        for _, r in gender_df.iterrows()
    ]

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>知乎用户画像分析平台</title>

<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>

<style>

body{
    margin:0;
    font-family:Microsoft YaHei;
    background:#f6f6f6;
}

/* ⭐标题居中 */
h1{
    text-align:center;
    padding:18px;
    color:#333;
    font-weight:600;
}

/* ⭐容器 */
.container{
    max-width:1200px;
    margin:auto;
    padding:20px;
}

/* ⭐2x2 */
.grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:18px;
}

/* ⭐卡片 */
.card{
    background:white;
    padding:18px;
    border-radius:14px;
    box-shadow:0 3px 12px rgba(0,0,0,0.06);
    text-align:center;
}

/* ⭐图表 */
.chart{
    width:100%;
    height:380px;
}

/* ⭐用户数卡片 */
.big-number{
    font-size:42px;
    font-weight:bold;
    color:#7892B5;
}

/* ⭐标题居中 */
.card h2{
    text-align:center;
    margin-bottom:10px;
    color:#555;
}

/* ⭐词云 */
img{
    width:100%;
    height:380px;
    object-fit:contain;
}

/* ⭐响应式 */
@media(max-width:900px){
    .grid{grid-template-columns:1fr;}
}

</style>
</head>

<body>

<h1>知乎用户画像大数据分析平台</h1>

<div class="container">

<div class="card">
<h2>总用户数</h2>
<div class="big-number">{{ total_user }}</div>
</div>

<div class="grid">

<div class="card">
<h2>性别分布</h2>
<div id="gender" class="chart"></div>
</div>

<div class="card">
<h2>回答数分布</h2>
<div id="answer" class="chart"></div>
</div>

<div class="card">
<h2>发文数分布</h2>
<div id="post" class="chart"></div>
</div>

<div class="card">
<h2>姓氏词云</h2>
<img src="/static/surname_wordcloud.png">
</div>

</div>

</div>

<script>

/* ⭐莫兰迪配色（你给的参考图） */
const palette = ['#E9B9AA','#D98481','#7892B5','#8CB9C0','#91B5A9','#EDCA7F'];

/* 性别 */
echarts.init(document.getElementById('gender')).setOption({
    color: palette,
    tooltip:{trigger:'item'},
    series:[{
        type:'pie',
        radius:'65%',
        data: {{ gender_data | tojson }}
    }]
});

/* 回答数 */
echarts.init(document.getElementById('answer')).setOption({
    color:'#7892B5',
    tooltip:{trigger:'axis'},
    xAxis:{type:'category',data:{{ answer_x | tojson }}},
    yAxis:{type:'value'},
    series:[{
        type:'bar',
        data:{{ answer_y | tojson }},
        barWidth:'50%'
    }]
});

/* 发文数 */
echarts.init(document.getElementById('post')).setOption({
    color:'#91B5A9',
    tooltip:{trigger:'axis'},
    xAxis:{type:'category',data:{{ post_x | tojson }}},
    yAxis:{type:'value'},
    series:[{
        type:'bar',
        data:{{ post_y | tojson }},
        barWidth:'50%'
    }]
});

</script>

</body>
</html>
"""

    return render_template_string(
        html,
        total_user=int(total_user),
        gender_data=gender_data,
        answer_x=answer_x,
        answer_y=answer_y,
        post_x=post_x,
        post_y=post_y
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
