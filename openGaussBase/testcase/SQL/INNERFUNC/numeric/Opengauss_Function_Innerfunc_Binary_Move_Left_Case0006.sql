-- @testpoint: 数字操作符<<(二进制左移), 最大整数进行左移
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
select clo1<< 10, clo2 <<10 from data_01;
drop table if exists data_01;