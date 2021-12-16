-- @testpoint: 数字操作符^(幂),指数为0或者底数为0
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (922337203685477580.6, 0);
select clo1 ^ clo2 from data_01;
SELECT 0 ^ 3 AS RESULT;
drop table if exists data_01;