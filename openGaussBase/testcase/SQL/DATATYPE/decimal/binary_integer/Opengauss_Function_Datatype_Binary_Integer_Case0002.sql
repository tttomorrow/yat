-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists binary_integer02;
create table binary_integer02 (name binary_integer);
drop table binary_integer02;