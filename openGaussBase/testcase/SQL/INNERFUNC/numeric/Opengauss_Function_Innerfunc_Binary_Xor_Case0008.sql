-- @testpoint: 数字操作符#(二进制XOR),空值进行数二进制xor
drop table if exists data_01;
create table data_01 (clo1 int,clo2 SMALLINT);
select clo1 # clo2 from data_01;
SELECT null # 10  AS RESULT;
drop table if exists data_01;