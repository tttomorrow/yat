-- @testpoint: div函数参数个数校验，合理报错
drop table if exists data_01;
create table data_01 (clo1 bigint,clo2 float);
select div (clo2) from data_01;
select div () as result;
drop table if exists data_01;