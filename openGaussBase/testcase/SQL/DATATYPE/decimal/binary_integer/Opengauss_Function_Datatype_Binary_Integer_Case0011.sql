-- @testpoint: 插入有效负整数

drop table if exists binary_integer11;
create table binary_integer11 (name binary_integer);
insert into binary_integer11 values (-123);
insert into binary_integer11 values (-12356);
insert into binary_integer11 values (-9999999);
select * from binary_integer11;
drop table binary_integer11;