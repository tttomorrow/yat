-- @testpoint: dec数据类型多次转换至FLOAT8

drop table if exists dec_10;
CREATE  TABLE dec_10 (id DEC(4,2));
insert into dec_10 values (11.11);

alter table dec_10 alter column id TYPE FLOAT8;
--查看字段类型转换是否成功
SELECT format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'dec_10' and a.attrelid = c.oid and a.attnum>0;
alter table dec_10 alter column id TYPE DEC(4,2);
alter table dec_10 alter column id TYPE FLOAT8;
alter table dec_10 alter column id TYPE DEC(4,2);

--查看字段类型转换是否成功
SELECT format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'dec_10' and a.attrelid = c.oid and a.attnum>0;
alter table dec_10 alter column id TYPE FLOAT8;
alter table dec_10 alter column id TYPE DEC(4,2);
alter table dec_10 alter column id TYPE FLOAT8;

--查看字段类型转换是否成功
SELECT format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'dec_10' and a.attrelid = c.oid and a.attnum>0;

select * from dec_10;
drop table dec_10;