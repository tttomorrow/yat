-- @testpoint: 数字操作符||/(立方根),负数进行开立方
drop table if exists data_01;
create table data_01 (clo1 float,clo2 int);
insert into data_01 values (-0.001, -126);
select ||/ clo1 from data_01;
SELECT ||/ -8 AS RESULT;
drop table if exists data_01;