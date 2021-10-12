-- @testpoint: 插入非法空值，合理报错

drop table if exists number_12;
create table number_12 (id int,name number);
insert into number_12 values (1,' ');
drop table number_12;