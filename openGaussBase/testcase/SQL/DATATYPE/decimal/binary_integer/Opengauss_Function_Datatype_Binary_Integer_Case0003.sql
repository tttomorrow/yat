-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists binary_integer03;
create table binary_integer03 (name binary_integer);
insert into binary_integer03 values (2147483648);
drop table binary_integer03;