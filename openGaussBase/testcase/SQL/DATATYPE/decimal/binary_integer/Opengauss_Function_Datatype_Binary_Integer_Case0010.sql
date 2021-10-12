-- @testpoint: 插入有效正整数

drop table if exists binary_integer10;
create table binary_integer10 (name binary_integer);
insert into binary_integer10 values (123);
insert into binary_integer10 values (122340);
insert into binary_integer10 values (99999999);
select * from binary_integer10;
drop table binary_integer10;