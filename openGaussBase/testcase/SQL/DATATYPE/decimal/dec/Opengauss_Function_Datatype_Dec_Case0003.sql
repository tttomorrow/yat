-- @testpoint: dec数据类型转换至varchar2,char，float8，tinyint
-- @modified at: 2020-11-23

drop table if exists dec_03;
create table dec_03 (id dec(4,2));
insert into dec_03 values (11.11);
select * from dec_03;
--修改dec类型为varchar2
alter table dec_03 alter column id type varchar2(200);
--查询字段修改是否成功
SELECT format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'dec_03' and a.attrelid = c.oid and a.attnum>0;
insert into dec_03 values (11.11);
select * from dec_03;

--修改dec类型为char
alter table dec_03 alter column id type char(100);
--查询字段修改是否成功
SELECT format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'dec_03' and a.attrelid = c.oid and a.attnum>0;
insert into dec_03 values (11.11);
select * from dec_03;

--修改dec类型为float8
alter table dec_03 alter column id type float8;
--查询字段修改是否成功
SELECT format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'dec_03' and a.attrelid = c.oid and a.attnum>0;
insert into dec_03 values (11.11);
select * from dec_03;

--修改dec类型为tinyint
alter table dec_03 alter column id type tinyint;
--查询字段修改是否成功
SELECT format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'dec_03' and a.attrelid = c.oid and a.attnum>0;
insert into dec_03 values (11.11);
select * from dec_03;

drop table dec_03;