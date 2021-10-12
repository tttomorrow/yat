-- @testpoint: 不指定精度，插入正整数

drop table if exists number_01;
create table number_01 (name number);
insert into number_01 values (123);
insert into number_01 values (9999999);
insert into number_01 values (1);
insert into number_01 values (2);
insert into number_01 values (3);
select * from number_01;
drop table number_01;