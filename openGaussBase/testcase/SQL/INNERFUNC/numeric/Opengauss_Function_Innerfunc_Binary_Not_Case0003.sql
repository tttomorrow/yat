-- @testpoint: 数字操作符~(二进制NOT), 0 空值进行二进制not
drop table if exists data_01;
create table data_01 (clo1 int,clo2 float);
insert into data_01(clo1) values (0);
select ~ clo1 , ~ clo2 from data_01;
SELECT ~0,~ null  AS RESULT;
drop table if exists data_01;