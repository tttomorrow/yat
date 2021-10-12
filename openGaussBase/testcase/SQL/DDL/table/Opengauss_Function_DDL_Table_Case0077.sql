-- @testpoint: 创建表设置(表级)外键，外键不支持

DROP TABLE IF EXISTS example;
DROP TABLE IF EXISTS t1 ;
CREATE TABLE example (
        a integer,
        b integer,
        c integer,
        PRIMARY KEY (b, c)
    );
CREATE TABLE t1 (
        a integer PRIMARY KEY,
        b integer,
        c integer,
        FOREIGN KEY (b, c) REFERENCES example (b, c)
    );
DROP TABLE IF EXISTS example CASCADE;
DROP TABLE IF EXISTS t1 ;