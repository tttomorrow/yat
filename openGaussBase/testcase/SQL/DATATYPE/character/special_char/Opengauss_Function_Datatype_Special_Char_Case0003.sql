-- @testpoint: 创建表，将“char”数据类型转换至VARCHAR2,char
-- @modified at: 2020-11-16

drop table if exists special_char_03;
CREATE  TABLE special_char_03 (id "char");
insert into special_char_03 values ('t');
alter table special_char_03 alter column id TYPE VARCHAR2(200);

--查询字段信息是否修改成功
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'special_char_03' and a.attrelid = c.oid and a.attnum>0;

select * from special_char_03;

drop table if exists special_char_03;
CREATE  TABLE special_char_03 (id "char");
insert into special_char_03 values ('t');
alter table special_char_03 alter column id TYPE char(10);

--查询字段信息是否修改成功
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'special_char_03' and a.attrelid = c.oid and a.attnum>0;

select * from special_char_03;

drop table special_char_03;