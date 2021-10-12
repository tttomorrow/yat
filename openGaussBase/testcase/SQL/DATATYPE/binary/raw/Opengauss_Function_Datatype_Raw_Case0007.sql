-- @testpoint: 插入非法空值，合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_raw07;
CREATE TABLE test_raw07 (name raw);

--插入数据
INSERT INTO test_raw07 VALUES (' ');

--插入失败，查看数据
select * from test_raw07;

--清理数据
DROP TABLE test_raw07;
