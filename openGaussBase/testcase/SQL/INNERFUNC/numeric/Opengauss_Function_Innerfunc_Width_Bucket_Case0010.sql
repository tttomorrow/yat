-- @testpoint: width_bucket函数b1、b2非数值类型，合理报错
drop table if exists data_01;
create table data_01 (clo1 char,clo2 boolean);
insert into data_01 values ('a',true);
select width_bucket(clo1,2,5,5) from data_01;
select width_bucket(clo2,-3,3,5) from data_01;
select width_bucket(null,-3,3,5) from data_01;
drop table if exists data_01;