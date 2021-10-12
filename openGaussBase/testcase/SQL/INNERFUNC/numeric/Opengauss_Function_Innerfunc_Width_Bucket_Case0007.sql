-- @testpoint: width_bucket函数op超出左右边界
drop table if exists data_01;
create table data_01 (clo1 float,clo2 float);
insert into data_01 values (-3.7,11.1);
select width_bucket(clo1,2,5,5) from data_01;
select width_bucket(clo2,-3,3,5) from data_01;
drop table if exists data_01;
