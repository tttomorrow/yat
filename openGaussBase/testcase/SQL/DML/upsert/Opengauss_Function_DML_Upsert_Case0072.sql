--  @testpoint:建表时指定两列是主键约束，合理报错
drop table if exists t03;
--col1 和col2列指定为主键
CREATE TABLE t03 (col1 INT DEFAULT 1 PRIMARY KEY, col2 INT PRIMARY KEY, col3 INT);