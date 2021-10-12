-- @testpoint: 数字操作符|/(平方根),可以进行开平方的正整数（无法开尽）
drop table if exists data_01;
create table data_01 (clo1 int,clo2 SMALLINT);
insert into data_01 values (251, 126.0);
select  |/clo1 from data_01;
select  |/clo2 from data_01;
SELECT |/ 101 AS RESULT;
drop table if exists data_01;