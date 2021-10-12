-- @testpoint: 插入0值

drop table if exists number_13;
create table number_13 (name number);
insert into number_13 values (0);
insert into number_13 values (0);
insert into number_13 values (0);
select * from number_13;
drop table number_13;