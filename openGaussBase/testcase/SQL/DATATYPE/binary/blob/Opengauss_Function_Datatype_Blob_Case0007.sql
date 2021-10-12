-- @testpoint: 插入非法空值，合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS test_blob07;
CREATE TABLE test_blob07 (name blob);

--插入数据
INSERT INTO test_blob07 VALUES (' ');

--插入失败，查看数据
select * from test_blob07;

--清理环境
DROP TABLE test_blob07;
