-- @testpoint: 创建列类型是浮点类型DOUBLE PRECISION、FLOAT8的表

drop table if exists table_1;
create table table_1(a DOUBLE PRECISION);
insert into table_1 values(123456478685686786.12689852536453563456);
select * from table_1;
drop table if exists table_1;
drop table if exists table_2;
create table table_2(a FLOAT8);
insert into table_2 values(123456467891011127.1787902566223457866);
select * from table_2;
drop table if exists table_2;