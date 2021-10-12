-- @testpoint: 插入空值

drop table if exists number_14;
create table number_14 (id int,name number);
insert into number_14 values (1,null);
insert into number_14 values (2,null);
select * from number_14;
drop table number_14;