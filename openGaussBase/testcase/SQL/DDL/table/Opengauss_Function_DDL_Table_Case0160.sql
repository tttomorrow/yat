-- @testpoint: 创建类型是大对象的列存表，不支持blob，合理报错
drop table if exists table_1;
create table table_1(a clob )with (ORIENTATION=COLUMN);
insert into table_1 values('1010'),('1001'),('1011'),('1111');
select * from table_1;
drop table if exists table_1;

drop table if exists table_2;
create table table_2(a blob )with (ORIENTATION=COLUMN);
drop table if exists table_2;