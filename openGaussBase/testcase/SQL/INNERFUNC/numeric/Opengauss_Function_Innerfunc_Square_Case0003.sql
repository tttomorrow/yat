-- @testpoint: 数字操作符|/(平方根),正的浮点数进行开平方
drop table if exists data_01;
create table data_01 (clo1 float,clo2 SMALLINT);
insert into data_01 values (0.01, 126.0);
select  |/clo1 from data_01;
select  |/clo2 from data_01;
SELECT |/ 1.25 AS RESULT;
drop table if exists data_01;