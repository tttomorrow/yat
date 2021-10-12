-- @testpoint: 数字操作符||/(立方根),空值进行开立方
drop table if exists data_01;
create table data_01 (clo1 int,clo2 int);
select ||/ clo1 from data_01;
SELECT ||/ null AS RESULT;
drop table if exists data_01;