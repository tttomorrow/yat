-- @testpoint: width_bucket函数入参为浮点型
drop table if exists data_01;
create table data_01 (clo1 float,clo2 float);
insert into data_01 values (2.8,-1.3);
select width_bucket(clo1,0,10.8,5.5) from data_01;
select width_bucket(clo2,-8,50,5) from data_01;
select width_bucket(2.0,10.8,5.5,5.5);
select width_bucket(-2.0,-10.8,0,5.5);
drop table if exists data_01;