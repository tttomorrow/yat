-- @testpoint: 创建列类型是整数类型integer类型的表,超边界时合理报错
drop table if exists table_1;
create table table_1(a INT4);
insert into table_1 values(-2147483648);
insert into table_1 values(1255345657);
insert into table_1 values(2147483647);
insert into table_1 values(-2147483649);
insert into table_1 values(2147483648);
select * from table_1;
drop table if exists table_1;