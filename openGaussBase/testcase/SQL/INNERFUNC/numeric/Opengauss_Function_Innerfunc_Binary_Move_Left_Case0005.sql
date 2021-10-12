-- @testpoint: 数字操作符<<(二进制左移), 正负数的左移为31位、32位、33位
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (1, -32767);
select  clo1<<30 , clo2 <<31 from data_01;
SELECT 1<<32 AS RESULT;
drop table if exists data_01;