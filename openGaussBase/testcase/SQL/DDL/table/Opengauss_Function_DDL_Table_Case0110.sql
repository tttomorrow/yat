-- @testpoint: 创建列类型是INTEGER的表，超出边界时合理报错
drop table if exists table_1;
create table table_1(a INTEGER);
insert into table_1 values(-2147483648);
insert into table_1 values(1255345657);
insert into table_1 values(2147483647);
--ERROR:  integer out of range

insert into table_1 values(-2147483649);
insert into table_1 values(2147483648);
select * from table_1;
drop table if exists table_1;