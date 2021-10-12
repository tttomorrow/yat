-- @testpoint: 数字操作符^(幂),底数或指数为浮点数
drop table if exists data_01;
create table data_01 (clo1 FLOAT(3),clo2 FLOAT4);
insert into data_01 values (255.00001, 67.123445);
select * from data_01;
select clo1^clo2 from data_01;
SELECT 2 ^ 1.214 AS RESULT;
SELECT 12.123 ^ 3 AS RESULT;
drop table if exists data_01;