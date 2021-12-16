-- @testpoint: 数字操作符/(除)，数值和0相除，0作分母时合理报错
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (922337203685477580.6, 2);
select clo1 / 0 from data_01;
SELECT 0 / 3 AS RESULT;
drop table if exists data_01;