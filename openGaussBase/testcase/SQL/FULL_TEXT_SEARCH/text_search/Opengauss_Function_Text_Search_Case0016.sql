--  @testpoint:更新表修改重写规则
--函数结合表测试
--创建schema
drop schema if exists tsearch cascade;
CREATE schema tsearch;
--建表
DROP TABLE if EXISTS tsearch.aliases;
CREATE TABLE tsearch.aliases (id int, t tsquery, s tsquery);
--插入数据
INSERT INTO tsearch.aliases VALUES(1, to_tsquery('supernovae'), to_tsquery('supernovae|sn'));
--修改s列
UPDATE tsearch.aliases SET s = to_tsquery('supernovae|sn & !nebulae') WHERE t = to_tsquery('supernovae');
--使用ts_rewrite函数查询
SELECT ts_rewrite(to_tsquery('supernovae & crab'), 'SELECT t, s FROM tsearch.aliases');
SELECT ts_rewrite('a & b'::tsquery, 'SELECT t,s FROM tsearch.aliases WHERE ''a & b''::tsquery @> t');
--删除表
DROP TABLE tsearch.aliases;
--删除schema
DROP SCHEMA tsearch;
