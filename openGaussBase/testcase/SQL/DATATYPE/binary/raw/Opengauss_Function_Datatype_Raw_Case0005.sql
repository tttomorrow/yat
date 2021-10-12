-- @testpoint: 插入bool类型,合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_raw05;
CREATE TABLE test_raw05 (name raw);

--插入数据
INSERT INTO test_raw05 VALUES (true);

--插入失败，查看数据
select * from test_raw05;

--清理数据
DROP TABLE test_raw05;