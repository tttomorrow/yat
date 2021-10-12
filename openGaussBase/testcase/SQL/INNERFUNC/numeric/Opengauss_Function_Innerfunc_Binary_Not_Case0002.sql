-- @testpoint: 数字操作符~(二进制NOT), 正负浮点数进行二进制not
drop table if exists data_01;
create table data_01 (clo1 float,clo2 float);
insert into data_01 values (255.5, -32767.7);
select ~ clo1 , ~ clo2 from data_01;
SELECT ~91.5,~ -15.7  AS RESULT;
drop table if exists data_01;