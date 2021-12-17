-- @testpoint: 创建浮点类型-BINARY_DOUBLE 的表
drop table if exists table_2;
create table table_2(a BINARY_DOUBLE);
insert into table_2 values(12345646842225156526.1787536902566223456);
select * from table_2;
drop table if exists table_2;