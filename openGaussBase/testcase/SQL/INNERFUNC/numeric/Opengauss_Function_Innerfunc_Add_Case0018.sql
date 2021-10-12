-- @testpoint: 数字操作符+，入参为空值
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
select clo1 + clo2 from data_01;
SELECT null + -1 AS RESULT;
drop table if exists data_01;