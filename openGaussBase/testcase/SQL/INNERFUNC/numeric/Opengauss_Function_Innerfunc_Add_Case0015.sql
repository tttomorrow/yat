-- @testpoint: 数字操作符+，多个数连续相加
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (255, 3);
select clo1 + clo2+12.555 from data_01;
SELECT 10 + 3+0.5 AS RESULT;
drop table if exists data_01;