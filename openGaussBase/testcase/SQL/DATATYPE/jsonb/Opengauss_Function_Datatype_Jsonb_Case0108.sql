-- @testpoint: 创建数据类型为json的列存表：不支持，合理报错

--列存表：不支持json类型
drop table if exists tab1081;
create table tab1081(id int,name varchar,message json) with(orientation=column);

--列存分区表表：不支持json类型
drop table if exists tab1082;
create table tab1082(id int,name varchar,message json)with(orientation=column)
partition by range(message)
(partition part_1 values less than(20),
 partition part_2 values less than(30),
 partition part_3 values less than(maxvalue));
 
--清理数据
drop table if exists tab1081;
drop table if exists tab1082;
