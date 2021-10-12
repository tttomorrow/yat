-- @testpoint: 数字操作符||/(立方根),整型数进行开立方
drop table if exists data_01;
create table data_01 (clo1 int,clo2 SMALLINT);
insert into data_01 values (8, 121.0);
select  ||/clo1 from data_01;
select  ||/clo2 from data_01;
SELECT ||/ 1000 AS RESULT;
drop table if exists data_01;