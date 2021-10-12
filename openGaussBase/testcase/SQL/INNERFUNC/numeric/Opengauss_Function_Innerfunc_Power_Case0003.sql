-- @testpoint: 数字操作符^(幂),底数或指数为负数
drop table if exists data_01;
create table data_01 (clo1 FLOAT(3),clo2 FLOAT4);
insert into data_01 values (-255, -67);
select * from data_01;
select clo1^clo2 from data_01;
SELECT -255.001 ^ -67 AS RESULT;
SELECT -2 ^ 3 AS RESULT;
drop table if exists data_01;