-- @testpoint: 插入数值，将name类型多次转换至varchar
-- @modified at: 2020-11-13


drop table if exists name_10;
CREATE TABLE name_10 (id name);
insert into name_10 values (10);
alter table name_10 alter column id TYPE varchar(64);
alter table name_10 alter column id TYPE name;
alter table name_10 alter column id TYPE varchar(64);

--查询字段信息是否转换成功
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'name_10' and a.attrelid = c.oid and a.attnum>0;

alter table name_10 alter column id TYPE name;
alter table name_10 alter column id TYPE varchar(64);
alter table name_10 alter column id TYPE name;

--查询字段信息是否转换成功
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'name_10' and a.attrelid = c.oid and a.attnum>0;

select * from name_10;
drop table name_10;