-- @testpoint: 数字操作符<<(二进制左移), 正负整数的左移（左移位数不超过31位）
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (255, -32767);
select  clo1<<5 , clo2 <<2 from data_01;
SELECT 1<<4 AS RESULT;
drop table if exists data_01;