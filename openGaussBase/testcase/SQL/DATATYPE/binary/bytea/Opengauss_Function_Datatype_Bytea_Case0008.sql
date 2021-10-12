-- @testpoint: 插入0值,合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_bytea08;
CREATE TABLE test_bytea08 (name bytea);

--插入数据
INSERT INTO test_bytea08 VALUES (0);

--插入成功，查看数据
select * from test_bytea08;

--清理环境
DROP TABLE test_bytea08;
