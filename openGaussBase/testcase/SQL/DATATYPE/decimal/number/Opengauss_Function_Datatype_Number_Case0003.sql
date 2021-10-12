-- @testpoint: 不指定精度，插入浮点数

drop table if exists number_03;
create table number_03 (name number);
insert into number_03 values (12122.12);
insert into number_03 values (0.000001);
insert into number_03 values (-12122.23);
insert into number_03 values (-0.000001);
select * from number_03;
drop table number_03;
