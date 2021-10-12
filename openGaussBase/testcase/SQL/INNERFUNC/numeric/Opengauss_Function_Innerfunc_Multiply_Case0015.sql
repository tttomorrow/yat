-- @testpoint: 数字操作符*(乘),0作为乘数
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
select clo1 * 0 from data_01;
drop table if exists data_01;