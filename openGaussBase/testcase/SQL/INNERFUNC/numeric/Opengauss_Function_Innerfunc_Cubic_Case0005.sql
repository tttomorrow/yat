-- @testpoint: 数字操作符||/(立方根),边界值进行开立方
drop table if exists data_01;
create table data_01 (clo1 int,clo2 BIGINT);
select ||/clo1,||/clo2 from data_01;
drop table if exists data_01;