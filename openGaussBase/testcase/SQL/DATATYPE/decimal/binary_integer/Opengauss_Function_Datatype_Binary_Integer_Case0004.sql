-- @testpoint: 插入右边界范围值

drop table if exists binary_integer04;
create table binary_integer04 (name binary_integer);
select * from binary_integer04;
drop table binary_integer04;