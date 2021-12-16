-- @testpoint: 数字操作符+，最大值相加
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (9223372036854775806, 1);
select clo1 + clo2 from data_01;
SELECT -9223372036854775806 + -1 AS RESULT;
drop table if exists data_01;