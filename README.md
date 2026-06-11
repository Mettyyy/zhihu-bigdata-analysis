# 知乎用户画像大数据分析平台 (Zhihu User Portrait Analysis System)



本项目为大数据与云计算课程的实验项目。系统基于 B/S 架构开发，实现了从原始 JSON 数据的分布式并行清洗、ETL 管道流转，到大规模多维指标聚合统计，再到基于 Web 端的纯前端实时动态可视化的全链路闭环流程。



---



## 🛠️ 技术栈 (Technology Stack)



* **数据清洗与 ETL**：Kettle (Pentaho Data Integration) —— 支持多核并行计算、内置计算因子及 JavaScript 自定义函数。

* **分布式统计分析**：Python 3 + PySpark (Apache Spark Core) —— 针对高并发、大规模数据的高效 MapReduce 聚合。

* **数据存储**：MySQL 5.6+ —— 解决远程连接权限，支撑中间干净数据与结果集的持久化。

* **Web 后端服务**：Flask (Python Web Framework) —— 轻量级 B/S 架构服务端。

* **前端数据可视化**：ECharts 5 + `echarts-wordcloud` 插件 —— **严格执行“禁止使用预生成图像”禁令**，全图表动态实时 Canvas/SVG 渲染，支持鼠标悬停动态交互。



---



## 📂 项目结构 (Project Structure)



```text

zuel_bigdata/

├── jars/                   # 存放 Spark 连接 MySQL 所需的依赖驱动

│   └── mysql-connector-java-8.0.26.jar

├── kettle/                 # Kettle ETL 转换流程配置文件

│   └── data_cleansing.ktr  # 包含去空、去重、JS提取姓氏及x4并行计算的核心流程

├── pyspark/                # 分布式统计分析模块

│   └── spark_analysis.py   # 性别、发文、回答、姓氏多维指标聚合计算脚本

├── sql/                    # 数据库初始化及表结构脚本

│   ├── create_database.sql # 原始表、清洗表及结果看板表的建表语句

├── web/                    # Flask Web 可视化平台

│   ├── static/

│   │   └── style.css       # 样式表

│   ├── templates/

│   │   └── index.html      # 纯前端 ECharts 动态渲染（含异步动态词云）

│   └── app.py              # Flask 核心路由与数据接口服务

└── README.md               # 项目说明文档



## 运行与操作指南 (Deployment & Execution)

 

### 阶段一：数据库初始化与环境准备

 

登录 MySQL 数据库，执行初始化脚本创建数据库及相关表结构（如 `user_raw_data`）：

 

```bash

mysql -uroot -p < sql/create_database.sql

```

 

---

 

### 阶段二：Kettle 数据清洗任务 (ETL)

 

打开 Kettle Spoon 客户端，加载 `kettle/data_cleansing.ktr` 流程。

 

**数据清洗核心逻辑：**

 

1. **去空与去负数异常**：通过内置计算因子 `过滤记录 (Filter rows)` 剔除 `name IS NULL` 以及发文/回答数为负数的脏数据。

2. **全局去重**：通过 `排序记录 (Sort rows)` 与 `唯一行 (Unique rows)` 组件基于 `name` 字段进行全局去重。

3. **自定义函数提取姓氏**：编写 `JavaScript 代码` 核心脚本，通过自定义函数 `name.substr(0, 1)` 实时提取姓氏字段 `surname`。

4. **性能优化**：右键点击 `JavaScript 代码` 步骤，开启"多核并行计算"（改变开始复制的数量为 `4`），压榨 CPU 性能。

点击运行，将清洗后的干净数据导入 `user_clean_data` 表。

 

---

 

### 阶段三：PySpark 分布式统计分析

 

使用 Spark 提交计算任务，读取清洗后的干净数据，分布式执行四项统计分析（发文数量分布、性别比例、姓氏频次、回答质量），并将统计结果写回 MySQL 的 `res_xxx_dist` 结果表中：

 

```bash

spark-submit \

  --jars jars/mysql-connector-java-8.0.26.jar \

  pyspark/spark_analysis.py

```

 

---

 

### 阶段四：Flask Web 服务部署

 

进入 Web 目录，启动 Flask 后端服务器，将多维统计结果以 B/S 架构实时渲染至前端：

 

```bash

cd web

python3 app.py

```
