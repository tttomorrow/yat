-- @testpoint: 表中插入数据，对char、varchar类型可以相互进行MODIFY 操作
drop table if exists t1 cascade;
create table t1(a CHAR,c VARCHAR(10));
--修改char为varchar
alter table t1 modify(a VARCHAR(6));

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 't1' and a.attrelid = c.oid and a.attnum>0;
--插入数据后修改varchar为char
insert into t1 values('ddddd',90);
alter table t1 modify(a char(6));

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 't1' and a.attrelid = c.oid and a.attnum>0;

drop table if exists t1 cascade;