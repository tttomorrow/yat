-- @testpoint: 数字操作符-,货币类型相减
drop table if exists data_01;
create table data_01 (clo1 money,clo2 money);
insert into data_01 values (12.34, 0.01);
select clo1  clo2 from data_01;
SELECT -92233720368547758.06  -0.01 AS RESULT;
drop table if exists data_01;