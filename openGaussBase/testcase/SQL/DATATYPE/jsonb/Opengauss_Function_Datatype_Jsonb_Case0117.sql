-- @testpoint: 创建数据类型为jsonb的列存表：不支持，合理报错

--列存表：不支持jsonb类型
drop table if exists tab1171;
create table tab1171(id int,name varchar,message jsonb) with(orientation=column);

--列存分区表表：不支持jsonb类型
drop table if exists tab1172;
create table tab1172(id int,name varchar,message jsonb)with(orientation=column)
partition by range(message)
(partition part_1 values less than(20),
 partition part_2 values less than(30),
 partition part_3 values less than(maxvalue));
 
--清理数据
drop table if exists tab1171;
drop table if exists tab1172;
