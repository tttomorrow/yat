-- @testpoint: 插入bool类型，合理报错

drop table if exists number_10;
create table number_10 (name number);
insert into number_10 values (false);
insert into number_10 values (true);
drop table number_10;