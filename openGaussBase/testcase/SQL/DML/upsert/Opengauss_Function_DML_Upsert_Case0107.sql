-- @testpoint: 创建列存表指定主键约束

drop table if exists mykey_0a;
create table mykey_0a
(
   name char(20) ,
   id int primary key ,
   address char(50)
) with (ORIENTATION = COLUMN) ;

drop table mykey_0a cascade;