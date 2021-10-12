-- @testpoint: 创建表，修改nchar数据类型
-- @modified at: 2020-11-16

drop table if exists test_nchar_10;
create table test_nchar_10 (name nchar(10));

alter table test_nchar_10 modify name nchar(1);

--查看属性是否修改
SELECT format_type(a.atttypid,a.atttypmod) as type
FROM pg_class as c,pg_attribute as a
where c.relname = 'test_nchar_10' and a.attrelid = c.oid and a.attnum>0;

drop table test_nchar_10;