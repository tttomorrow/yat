-- @testpoint: 插入右边界范围值

drop table if exists binary_double09;
create table binary_double09 (name binary_double);
insert into binary_double09 values (1E+308);
select * from binary_double09;
drop table binary_double09;