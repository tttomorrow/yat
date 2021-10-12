-- @testpoint: 数字操作符!(阶乘),1或者0的阶乘
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (0, 1);
select  clo1! from data_01;
select  clo2! from data_01;
SELECT 1! AS RESULT;
drop table if exists data_01;