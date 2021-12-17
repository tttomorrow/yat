-- @testpoint: 数字操作符/(除)，相除结果超出被除数类型范围
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 float);
insert into data_01 values (9223372036854775806, 0.02);
select clo1 / clo2 from data_01;
SELECT -9223372036854775806 / 2 AS RESULT;
drop table if exists data_01;