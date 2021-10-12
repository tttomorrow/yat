-- @testpoint: 数字操作符#(二进制XOR),二进制xor操作符连续使用
drop table if exists data_01;
create table data_01 (clo1 int,clo2 SMALLINT,clo3 SMALLINT);
insert into data_01 values (10, 3276, 7);
select clo1 # clo2 # clo3 from data_01;
SELECT 11 # 11 # 11  AS RESULT;
SELECT 0 # 10 # 22 # 5   AS RESULT;
drop table if exists data_01;