-- @testpoint: 数字操作符#(二进制XOR),精度不同的浮点型进行二进制xor
drop table if exists data_01;
create table data_01 (clo1 float,clo2 float);
insert into data_01 values (1.25, 2.45);
select clo1 # clo2 from data_01;
SELECT 1.26 # -15  AS RESULT;
SELECT 8.81 # 0  AS RESULT;
drop table if exists data_01;