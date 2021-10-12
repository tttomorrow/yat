-- @testpoint: 插入空值
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_blob09;
CREATE TABLE test_blob09 (name blob);

--插入数据
INSERT INTO test_blob09 VALUES (null);

--插入成功，查看数据
select * from test_blob09;

--清理环境
DROP TABLE test_blob09;