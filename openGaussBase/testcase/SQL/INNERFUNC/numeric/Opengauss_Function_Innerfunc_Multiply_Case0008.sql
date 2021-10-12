-- @testpoint: 数字操作符*(乘),正整数相乘
drop table if exists data_01;
create table data_01 (clo1 int,clo2 SMALLINT);
insert into data_01 values (255, 32767);
select clo1 * clo2 from data_01;
SELECT 10*32768 AS RESULT;
drop table if exists data_01;