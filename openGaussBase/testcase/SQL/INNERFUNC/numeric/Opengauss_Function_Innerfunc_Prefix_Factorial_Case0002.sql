-- @testpoint: 数字操作符!!(前缀阶乘),浮点型数据的阶乘
drop table if exists data_01;
create table data_01 (clo1 float,clo2 float);
insert into data_01 values (8.1, 2.0);
select  !!clo1 from data_01;
select  !!clo2 from data_01;
SELECT !!5.5 AS RESULT;
drop table if exists data_01;