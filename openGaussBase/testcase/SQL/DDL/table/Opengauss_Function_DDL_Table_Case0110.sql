-- @testpoint: 创建列类型是INTEGER的表，超出边界时合理报错
drop table if exists table_1;
create table table_1(a INTEGER);
--ERROR:  integer out of range

select * from table_1;
drop table if exists table_1;