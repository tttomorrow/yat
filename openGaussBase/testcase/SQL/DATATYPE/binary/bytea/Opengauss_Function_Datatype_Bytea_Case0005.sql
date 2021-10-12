-- @testpoint: 插入bool类型,合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_bytea05;
CREATE TABLE test_bytea05 (name bytea);

--插入数据
INSERT INTO test_bytea05 VALUES (true);

--插入失败，查看数据
select * from test_bytea05;

--清理环境
DROP TABLE test_bytea05;