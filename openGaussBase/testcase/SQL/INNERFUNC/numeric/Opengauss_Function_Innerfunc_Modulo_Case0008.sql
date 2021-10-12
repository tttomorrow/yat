-- @testpoint: 数字操作符%(求余),给空值求模
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
select clo1 % 3 from data_01;
SELECT null % 3 AS RESULT;
drop table if exists data_01;