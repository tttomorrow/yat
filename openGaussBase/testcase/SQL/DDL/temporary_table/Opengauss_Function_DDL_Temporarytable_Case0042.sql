-- @testpoint: 创建临时表，表名中有汉字和特殊字符，合理报错
-- @modify at: 2020-11-24
drop table if exists temporary_万@$#1;
create  temporary table temporary_万@$#1(a int);


