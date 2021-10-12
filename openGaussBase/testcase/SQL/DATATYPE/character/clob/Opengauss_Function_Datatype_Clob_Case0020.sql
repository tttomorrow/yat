--  @testpoint:clob:隐式转换支持char/varchar2转为clob:success
--建表
drop table if exists test_clob_20 CASCADE;
create table test_clob_20(id int,name clob);
--插入数据
--char
insert into test_clob_20 VALUES(1, cast('t' as char));
--varchar2
insert into test_clob_20 VALUES(2, cast('test_clob' as varchar2));

--查询字段信息
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_20' and a.attrelid = c.oid and a.attnum>0;

--清理数据
drop table if exists test_clob_20 CASCADE;