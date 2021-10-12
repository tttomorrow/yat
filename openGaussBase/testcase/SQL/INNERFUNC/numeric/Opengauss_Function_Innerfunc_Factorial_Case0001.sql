-- @testpoint: 数字操作符!(阶乘),正整数的阶乘
drop table if exists data_01;
create table data_01 (clo1 int,clo2 SMALLINT);
insert into data_01 values (8, 2);
select  clo1! from data_01;
select  clo2! from data_01;
SELECT 5! AS RESULT;
drop table if exists data_01;