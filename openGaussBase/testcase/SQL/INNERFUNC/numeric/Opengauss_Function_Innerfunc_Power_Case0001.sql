-- @testpoint: 数字操作符^(幂),正整数的幂
drop table if exists data_01;
create table data_01 (clo1 int,clo2 SMALLINT);
insert into data_01 values (2, 5);
select  clo1^clo2 from data_01;
SELECT 2^3 AS RESULT;
drop table if exists data_01;