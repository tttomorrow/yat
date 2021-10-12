-- @testpoint: 数字操作符~(二进制NOT), 对运算表达式进行取反
drop table if exists data_01;
create table data_01 (clo1 INT,clo2 INT);
insert into data_01 values (92, 125);
select ~ (clo1+clo2) from data_01;
SELECT ~922-20*3 AS RESULT;
drop table if exists data_01;