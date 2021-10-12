-- @testpoint: 插入正常数值，将name类型转换为VARCHAR2,char
-- @modified at: 2020-11-13

drop table if exists name_03;
CREATE  TABLE name_03 (id name);
insert into name_03 values (11.11);
alter table name_03 alter column id type varchar2(200);
select * from name_03;
--查询字段信息是否转换成功
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'name_03' and a.attrelid = c.oid and a.attnum>0;
drop table name_03;

CREATE TABLE name_03 (id name);
insert into name_03 values (11.11);
alter table name_03 alter column id TYPE char(10);
--查询字段信息是否转换成功
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'name_03' and a.attrelid = c.oid and a.attnum>0;
select * from name_03;
drop table name_03;