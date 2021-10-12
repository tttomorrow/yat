-- @testpoint: 数字操作符!(阶乘),阶乘结果过大溢出，合理报错
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
select  clo1! from data_01;
select  clo2! from data_01;
drop table if exists data_01;