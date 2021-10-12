-- @testpoint: width_bucket函数op处于里桶的边界
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (3,1);
select width_bucket(clo1,1,4,3) from data_01;
select width_bucket(clo2,-3,3,6) from data_01;
drop table if exists data_01;