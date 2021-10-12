-- @testpoint: 插入有效负整数

drop table if exists binary_double02;
create table binary_double02 (name binary_double);
insert into binary_double02 values (-12121);
insert into binary_double02 values (-000123);
select * from binary_double02;
drop table binary_double02;
