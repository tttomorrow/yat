-- @testpoint: 创建列类型是浮点类型DOUBLE PRECISION、FLOAT8的表

drop table if exists table_1;
create table table_1(a DOUBLE PRECISION);
select * from table_1;
drop table if exists table_1;
drop table if exists table_2;
create table table_2(a FLOAT8);
select * from table_2;
drop table if exists table_2;