-- @testpoint: 修改主键的数据类型为本身类型，改变长度
drop table if exists t1 cascade;
create table t1(a CHAR,c VARCHAR(10));

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 't1' and a.attrelid = c.oid and a.attnum>0;

alter table t1 MODIFY (a char(2));

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 't1' and a.attrelid = c.oid and a.attnum>0;

drop table if exists t1 cascade;