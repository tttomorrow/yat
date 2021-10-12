-- @testpoint: 创建临时表，字段名中有特殊字符，合理报错
-- @modify at: 2020-11-24
--建表，报错
drop table if exists temporary_1;
create  temporary table temporary_1(#！ int);
create  temporary table temporary_1($！ int);
create  temporary table temporary_1($@&^ int);

