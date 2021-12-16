-- @testpoint: 数字操作符*(乘),0作为乘数
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (922337203685477580.6, 2);
select clo1 * 0 from data_01;
SELECT -9223372036854775806 * 0 AS RESULT;
drop table if exists data_01;