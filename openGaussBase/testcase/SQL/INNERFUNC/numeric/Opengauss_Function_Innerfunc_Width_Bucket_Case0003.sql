-- @testpoint: width_bucket函数op处于左边界
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (2,-3);
select width_bucket(clo1,2,5,5) from data_01;
select width_bucket(clo2,-3,0,5) from data_01;
select width_bucket(3,3,5,5);
select width_bucket(-1,-1,0,5);
drop table if exists data_01;