-- @testpoint: 数字操作符*(乘),最大值相乘超出范围，合理报错
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
select clo1 * clo2 from data_01;
drop table if exists data_01;