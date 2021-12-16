-- @testpoint: 创建列类型是浮点类型REAL、FLOAT4的表
drop table if exists table_1;
create table table_1(a real);
insert into table_1 values(12345646.123456);
select * from table_1;
drop table if exists table_1;
drop table if exists table_2;
create table table_2(a FLOAT4);
insert into table_2 values(12345646842225.1787902566223456);
select * from table_2;
drop table if exists table_2;