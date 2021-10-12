-- @testpoint: 插入有效正整数

drop table if exists binary_double01;
create table binary_double01 (name binary_double);
insert into binary_double01 values (120);
insert into binary_double01 values (000123);
select * from binary_double01;
drop table binary_double01;