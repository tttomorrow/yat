--  @testpoint: clob：存储长度:1个字节：success
drop table if exists test_clob_13 CASCADE;
create table test_clob_13(name clob);
--插入数据
INSERT INTO test_clob_13 values('a');
--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_13' and a.attrelid = c.oid and a.attnum>0;
--清理数据
drop table if exists test_clob_13 CASCADE;