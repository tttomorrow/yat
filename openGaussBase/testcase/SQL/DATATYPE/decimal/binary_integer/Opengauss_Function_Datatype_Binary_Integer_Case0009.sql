-- @testpoint: 插入0值

drop table if exists binary_integer09;
create table binary_integer09 (name binary_integer);
insert into binary_integer09 values (0);
select * from binary_integer09;
drop table binary_integer09;