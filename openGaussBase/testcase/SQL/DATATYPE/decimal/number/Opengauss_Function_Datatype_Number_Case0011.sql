-- @testpoint: 插入指数形式值

drop table if exists number_11;
create table number_11 (name number);
insert into number_11 values (exp(33));
insert into number_11 values (exp(1.233));
insert into number_11 values (exp(-15));
insert into number_11 values (exp(-1.5));
select * from number_11;
drop table number_11;