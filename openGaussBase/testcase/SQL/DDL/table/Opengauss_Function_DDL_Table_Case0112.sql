-- @testpoint: 创建列类型是整数类型BIGINT的表，超边界时合理报错
drop table if exists table_1;
create table table_1(a BIGINT);
--ERROR:  bigint out of range
select * from table_1;
drop table if exists table_1;