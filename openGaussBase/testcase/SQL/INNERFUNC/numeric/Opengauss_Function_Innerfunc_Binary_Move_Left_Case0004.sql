-- @testpoint: 数字操作符<<(二进制左移), 左移的位数为小数负数
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (1, -32767);
select  clo1<<5.56 , clo2 <<-5 from data_01;
SELECT 1<<4.1 AS RESULT;
drop table if exists data_01;