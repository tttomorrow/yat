-- @testpoint: 数字操作符%(求余),非数值类型求模，合理报错
drop table if exists data_01;
create table data_01 (clo1 int,clo2 char);
insert into data_01 values (255, 'A');
select clo1 % clo2 from data_01;
SELECT 10 % 'a' AS RESULT;
drop table if exists data_01;