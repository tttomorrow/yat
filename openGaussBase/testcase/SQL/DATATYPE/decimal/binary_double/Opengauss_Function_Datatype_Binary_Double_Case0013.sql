-- @testpoint: 插入非法空值，合理报错

drop table if exists binary_double13;
create table binary_double13 (id int,name binary_double);
insert into binary_double13 values (1,' ');
drop table binary_double13;