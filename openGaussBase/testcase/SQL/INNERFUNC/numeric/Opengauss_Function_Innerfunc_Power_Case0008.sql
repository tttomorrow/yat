-- @testpoint: 数字操作符^(幂),指数为空值或者底数为空值
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
select clo1 ^ 3 from data_01;
SELECT null ^ 3 AS RESULT;
SELECT 3 ^ null AS RESULT;
drop table if exists data_01;