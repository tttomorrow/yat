-- @testpoint: width_bucket函数入参为整数型
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (2,-3);
select width_bucket(clo1,0,5,5) from data_01;
select width_bucket(clo2,-7,0,5) from data_01;
select width_bucket(3,0,5,5);
select width_bucket(-1,-5,0,5);
drop table if exists data_01;