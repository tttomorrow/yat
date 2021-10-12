-- @testpoint: 不指定精度，插入负整数

drop table if exists number_02;
create table number_02 (name number);
insert into number_02 values (-1212);
insert into number_02 values (-99999999);
insert into number_02 values (-1);
insert into number_02 values (-2);
insert into number_02 values (-3);
select * from number_02;
drop table number_02;
