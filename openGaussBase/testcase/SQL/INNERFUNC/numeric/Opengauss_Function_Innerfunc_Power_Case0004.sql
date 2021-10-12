-- @testpoint: 数字操作符^(幂),非法值校验，合理报错
drop table if exists data_01;
create table data_01 (clo1 int,clo2 char);
insert into data_01 values (255, 'A');
select  clo2 ^ clo1 from data_01;
SELECT 10 ^ 'a' AS RESULT;
drop table if exists data_01;