--  @testpoint: clob：建表作为数据类型：行存local临时表：success
drop table if exists test_clob_02 CASCADE;
create LOCAL TEMPORARY table test_clob_02(name clob) ;
--插入数据
INSERT INTO test_clob_02 values('test_clob');
--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_02' and a.attrelid = c.oid and a.attnum>0;
--清理数据
drop table if exists test_clob_02 CASCADE;