-- @testpoint: 插入指数形式值，合理报错
-- @modify at: 2020-11-04


--创建表
DROP TABLE IF EXISTS test_bytea06;
CREATE TABLE test_bytea06 (name bytea);

--插入数据
INSERT INTO test_bytea06 VALUES (exp(3));

--插入失败，查看数据
select * from test_bytea06;

--清理环境
DROP TABLE test_bytea06;
