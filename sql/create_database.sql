CREATE DATABASE IF NOT EXISTS bigdata_db
DEFAULT CHARACTER SET utf8mb4;

USE bigdata_db;

DROP TABLE IF EXISTS user_raw_data;

CREATE TABLE user_raw_data(
    answer_count VARCHAR(50),
    articles_count VARCHAR(50),
    gender VARCHAR(20),
    name VARCHAR(255)
);

DROP TABLE IF EXISTS res_gender_dist;

CREATE TABLE res_gender_dist(
    gender_label VARCHAR(20),
    count INT
);

DROP TABLE IF EXISTS res_answer_dist;

CREATE TABLE res_answer_dist(
    answer_range VARCHAR(20),
    count INT
);

DROP TABLE IF EXISTS res_post_dist;

CREATE TABLE res_post_dist(
    post_range VARCHAR(20),
    count INT
);

DROP TABLE IF EXISTS res_surname_dist;

CREATE TABLE res_surname_dist(
    surname VARCHAR(20),
    cnt INT
);

DROP TABLE IF EXISTS res_surname_top10;

CREATE TABLE res_surname_top10(
    surname VARCHAR(20),
    cnt INT
);
