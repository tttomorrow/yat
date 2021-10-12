--  @testpoint: clob:隐式转换支持clob转为char/varchar2/number:success
--建表
drop table if exists test_clob_21 CASCADE;
create table test_clob_21(id int,name1 char, name2 varchar2, name3 number);
--插入数据



--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_21' and a.attrelid = c.oid and a.attnum>0;

--清理数据
drop table if exists test_clob_21 CASCADE;