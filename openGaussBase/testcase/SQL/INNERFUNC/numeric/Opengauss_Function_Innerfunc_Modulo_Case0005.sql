-- @testpoint: 数字操作符%(求余),多个数连续求余
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (255, 3);
select clo1 * (2.5 + clo2+12.555)%clo2 from data_01;
SELECT 10 % (2.5  + 3+0.5) AS RESULT;
drop table if exists data_01;