-- @testpoint: 创建列类型是货币类型的列存表
drop table if exists table_2;
create table table_2(a money)with (ORIENTATION=COLUMN);
insert into table_2 values(123.253),(124.253),(125.253);
select * from table_2;
drop table if exists table_2;