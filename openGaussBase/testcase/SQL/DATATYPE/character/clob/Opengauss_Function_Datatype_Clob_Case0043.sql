--  @testpoint: --clob：建列存临时表后alter增加clob数据类型
drop table if exists test_clob_43;
create TEMPORARY table test_clob_43(id int) with(orientation = column);
alter table test_clob_43 add column name clob;

--查询字段信息
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_clob_43' and a.attrelid = c.oid and a.attnum>0;

--清理数据
drop table if exists test_clob_43;