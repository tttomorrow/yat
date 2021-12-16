-- @testpoint: 创建列类型是整数类型BIGINT的表，超边界时合理报错
drop table if exists table_1;
create table table_1(a BIGINT);
insert into table_1 values(-9223372036854775808);
insert into table_1 values(4255345657233445657);
insert into table_1 values(9223372036854775807);
--ERROR:  bigint out of range
insert into table_1 values(-9223372036854775809);
insert into table_1 values(9223372036854775808);
select * from table_1;
drop table if exists table_1;