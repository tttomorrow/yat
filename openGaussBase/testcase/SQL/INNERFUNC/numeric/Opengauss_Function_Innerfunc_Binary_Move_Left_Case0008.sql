-- @testpoint: 数字操作符<<(二进制左移), 空值进行左移
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 char);
select clo1<< 10, clo2 <<10 from data_01;
SELECT null << 10  AS RESULT;
drop table if exists data_01;