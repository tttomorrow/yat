-- @testpoint: 插入0值,合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_raw08;
CREATE TABLE test_raw08 (name raw);

--插入数据
INSERT INTO test_raw08 VALUES (0);

--清理环境
DROP TABLE test_raw08;