-- @testpoint: 数字操作符#(二进制XOR),边界值进行二进制xor
drop table if exists data_01;
create table data_01 (clo1 BIGINT,clo2 BIGINT);
insert into data_01 values (9223372036854775807, 9223372036854775807);
select clo1 # clo2 from data_01;
SELECT 9223372036854775807 # -9223372036854775807  AS RESULT;
SELECT 9223372036854775807 # 0.001 AS RESULT;
drop table if exists data_01;