-- @testpoint: 插入右边界范围值

drop table if exists binary_integer04;
create table binary_integer04 (name binary_integer);
insert into binary_integer04 values (2147483647);
select * from binary_integer04;
drop table binary_integer04;