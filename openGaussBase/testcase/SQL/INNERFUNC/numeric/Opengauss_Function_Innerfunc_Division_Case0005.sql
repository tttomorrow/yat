-- @testpoint: 数字操作符/(除)，算术表达式作除数或被除数
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
insert into data_01 values (255, 3);
select clo1 * (2.5 + clo2+12.555)/clo2 from data_01;
SELECT 10 / (2.5  + 3+0.5) AS RESULT;
drop table if exists data_01;