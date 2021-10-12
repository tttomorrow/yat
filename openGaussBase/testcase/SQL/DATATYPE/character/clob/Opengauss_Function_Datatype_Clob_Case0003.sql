--  @testpoint: clob：建表作为数据类型：行存global临时表：success
--drop global temporary table if exists test_clob_03 CASCADE;
create global TEMPORARY table test_clob_03(name clob) ;
--插入数据
INSERT INTO test_clob_03 values('test_clob');
--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_03' and a.attrelid = c.oid and a.attnum>0;
--清理数据
drop table if exists test_clob_03 CASCADE;
