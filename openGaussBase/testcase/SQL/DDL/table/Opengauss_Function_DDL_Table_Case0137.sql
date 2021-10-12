-- @testpoint: 创建列类型为二进制类型bytea的表
drop table if exists table_2;
create table table_2(a BYTEA);
insert into table_2 values('0xDEADBEEF');
select * from table_2;
drop table if exists table_2;
