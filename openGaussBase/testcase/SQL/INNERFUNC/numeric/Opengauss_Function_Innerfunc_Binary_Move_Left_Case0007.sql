-- @testpoint: 数字操作符<<(二进制左移), 非法值校验，合理报错
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 char);
insert into data_01 values (123, 'a');
select clo1<< 10, clo2 <<10 from data_01;
SELECT 'A' << 10  AS RESULT;
SELECT 'A'<<10 AS RESULT;
drop table if exists data_01;