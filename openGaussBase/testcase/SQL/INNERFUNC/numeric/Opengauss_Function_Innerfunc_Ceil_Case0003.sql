-- @testpoint: ceil函数入参给非数值类型，合理报错
drop table if exists data_01;
create table data_01 (clo1 char,clo2 date);
insert into data_01 values ('a','2020-01-12');
select ceil(clo1), ceil(clo2) from data_01;
drop table if exists data_01;