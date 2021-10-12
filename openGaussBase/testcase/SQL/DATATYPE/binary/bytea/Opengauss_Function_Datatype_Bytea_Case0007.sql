-- @testpoint: 插入非法空值
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_bytea07;
CREATE TABLE test_bytea07 (name bytea);

--插入数据
INSERT INTO test_bytea07 VALUES (' ');

--插入成功，查看数据
select * from test_bytea07;

--清理环境
DROP TABLE test_bytea07;
