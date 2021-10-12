-- @testpoint: 插入非法空值,合理报错

drop table if exists binary_integer08;
create table binary_integer08 (id int,name binary_integer);
insert into binary_integer08 values (1,' ');
drop table binary_integer08;