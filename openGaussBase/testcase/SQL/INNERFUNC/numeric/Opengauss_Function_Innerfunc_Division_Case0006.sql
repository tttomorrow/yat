-- @testpoint: 数字操作符/(除)，相除结果超出被除数类型范围
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 float);
select clo1 / clo2 from data_01;
drop table if exists data_01;