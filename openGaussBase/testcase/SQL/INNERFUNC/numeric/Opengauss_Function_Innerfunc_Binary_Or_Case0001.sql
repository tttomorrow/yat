-- @testpoint: 数字操作符|(二进制OR), 两个正整数二进制or
drop table if exists data_01;
create table data_01 (clo1 int,clo2 SMALLINT);
insert into data_01 values (255, 32767);
select clo1 | clo2 from data_01;
SELECT 91|15  AS RESULT;
drop table if exists data_01;