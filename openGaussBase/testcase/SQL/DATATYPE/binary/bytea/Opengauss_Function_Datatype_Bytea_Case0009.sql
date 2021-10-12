-- @testpoint: 插入空值
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_bytea09;
CREATE TABLE test_bytea09 (name bytea);

--插入数据
INSERT INTO test_bytea09 VALUES (null);

--插入成功，查看数据
select * from test_bytea09;

--清理环境
DROP TABLE test_bytea09;