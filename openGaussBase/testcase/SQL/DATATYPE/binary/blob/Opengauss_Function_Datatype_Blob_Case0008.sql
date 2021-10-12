-- @testpoint: 插入0值,合理报错
-- @modify at: 2020-11-04


--创建表
DROP TABLE IF EXISTS test_blob08;
CREATE TABLE test_blob08 (name blob);

--插入数据
INSERT INTO test_blob08 VALUES (0);

--清理环境
DROP TABLE test_blob08;