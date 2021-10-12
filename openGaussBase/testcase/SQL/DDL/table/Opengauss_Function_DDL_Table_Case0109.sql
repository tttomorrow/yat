-- @testpoint: 创建列类型是SMALLINT的表，超出边界时合理报错
drop table if exists table_1;
create table table_1(a SMALLINT);
insert into table_1 values(-32768);
insert into table_1 values(12553);
insert into table_1 values(32767);
--ERROR:  smallint out of range
insert into table_1 values(-32769);
insert into table_1 values(32768);
select * from table_1;
drop table if exists table_1;