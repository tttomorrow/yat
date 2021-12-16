-- @testpoint: 创建列类型是浮点类型FLOAT[(p)]的表，p为非正整数时合理报错
--   如不指定精度，内部用DOUBLE PRECISION表示。）


drop table if exists table_1;
create table table_1(a FLOAT);
insert into table_1 values(12345646842225.1787902566223456);
select * from table_1;
drop table if exists table_1;

drop table if exists table_2;
create table table_2(a FLOAT(20));
insert into table_2 values(123456467891011127.1787902566223457866);
select * from table_2;
drop table if exists table_2;

drop table if exists table_3;
create table table_3(a FLOAT(53));
insert into table_3 values(123456467891011127.1787902566223457866);
select * from table_3;
drop table if exists table_3;

--ERROR:  precision for type float must be less than 54 bits
create table table_3(a FLOAT(54));
--ERROR:  precision for type float must be at least 1 bits
create table table_3(a FLOAT(0));

