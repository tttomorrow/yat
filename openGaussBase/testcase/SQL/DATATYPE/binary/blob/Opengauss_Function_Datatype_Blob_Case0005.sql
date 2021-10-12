-- @testpoint: 插入bool类型，合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_blob05;
CREATE TABLE test_blob05 (name blob);

--插入数据
INSERT INTO test_blob05 VALUES (true);

--插入失败，查看数据
select * from test_blob05;

--清理环境
DROP TABLE test_blob05;