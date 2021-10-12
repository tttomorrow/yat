--  @testpoint:查询重写相关函数测试
--ts_rewrite
SELECT ts_rewrite('a & b'::tsquery, 'a'::tsquery, 'c'::tsquery);
SELECT ts_rewrite('world'::tsquery, 'select ''world''::tsquery, ''hello''::tsquery');
--函数结合表测试
--创建schema
drop schema if exists tsearch cascade;
CREATE schema tsearch;
--建表
DROP TABLE if EXISTS tsearch.aliases;
CREATE TABLE tsearch.aliases (id int, t tsquery, s tsquery);
--插入数据
INSERT INTO tsearch.aliases VALUES(1, to_tsquery('supernovae'), to_tsquery('supernovae|sn'));
--使用ts_rewrite函数查询
SELECT ts_rewrite(to_tsquery('supernovae & crab'), 'SELECT t, s FROM tsearch.aliases');
--删除表
DROP TABLE tsearch.aliases;
--删除schema
DROP SCHEMA tsearch;
