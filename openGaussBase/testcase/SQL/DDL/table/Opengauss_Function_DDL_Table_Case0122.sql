-- @testpoint: 创建浮点类型-BINARY_DOUBLE 的表
drop table if exists table_2;
create table table_2(a BINARY_DOUBLE);
select * from table_2;
drop table if exists table_2;