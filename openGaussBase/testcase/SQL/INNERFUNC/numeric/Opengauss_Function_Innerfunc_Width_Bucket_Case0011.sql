-- @testpoint: width_bucket函数b2<=b1,相等时合理报错
drop table if exists data_01;
create table data_01 (clo1 char,clo2 boolean);
insert into data_01 values ('a',true);
select width_bucket(0,3,1,5) from data_01;
select width_bucket(5,9,1,5) from data_01;
select width_bucket(0,-3,-3,5) from data_01;
drop table if exists data_01;