-- @testpoint: 创建列类型是数值类型的列存表
drop table if exists table_1;
create table table_1(a integer,b decimal,c serial)with (ORIENTATION=COLUMN);
insert into table_1 values(123,253,963);
select * from table_1;
drop table if exists table_1;