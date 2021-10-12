-- @testpoint: 创建表，将“char”多次转换至VARCHAR

drop table if exists special_char_08;
CREATE  TABLE special_char_08 (id "char");
insert into special_char_08 values ('1');

alter table special_char_08 alter column id TYPE VARCHAR(1);
alter table special_char_08 alter column id TYPE "char";
alter table special_char_08 alter column id TYPE VARCHAR(1);

--查看字段类型是否修改成功
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'special_char_08' and a.attrelid = c.oid and a.attnum>0;

alter table special_char_08 alter column id TYPE "char";
alter table special_char_08 alter column id TYPE VARCHAR(1);
alter table special_char_08 alter column id TYPE "char";

--查看字段类型是否修改成功
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'special_char_08' and a.attrelid = c.oid and a.attnum>0;

select * from special_char_08;
drop table if exists special_char_08;