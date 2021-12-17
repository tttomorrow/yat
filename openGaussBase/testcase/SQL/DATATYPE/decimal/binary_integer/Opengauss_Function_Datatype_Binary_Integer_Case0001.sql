-- @testpoint: 插入左边界范围值

drop table if exists binary_integer01;
create table binary_integer01 (name binary_integer);
insert into binary_integer01 values (-2147483648 );
select * from binary_integer01;
drop table binary_integer01;