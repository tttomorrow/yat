-- @testpoint: 创建列类型是序列整型-SMALLSERIAL的表，超边界时合理报错
drop table if exists table_1;
create table table_1(a SMALLSERIAL);
insert into table_1 values(1);
insert into table_1 values(15234);
insert into table_1 values(32767);
--ERROR:  integer out of range
insert into table_1 values(0);
insert into table_1 values(32768);
select * from table_1;
drop table if exists table_1;
