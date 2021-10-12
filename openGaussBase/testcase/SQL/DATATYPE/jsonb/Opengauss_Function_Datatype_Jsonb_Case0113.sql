-- @testpoint: 普通表使用数据类型为json的列创建主外键，不支持，合理报错

--创建普通列存表创建主键
drop table if exists tab1131;
create table tab1131(id int,name varchar,message json primary key);
drop table if exists tab1132;
create table tab1132(id int,name varchar,message json, primary key(message));

--创建普通列存表创建外键
drop table if exists tab1133;
drop table if exists tab1134;
create table tab1133(a int primary key, b json,c integer);
create table tab1134(a int, b json,c integer,  foreign key(a) references  tab1133(a));

drop table if exists tab1135;
drop table if exists tab1136;
create table tab1135(a json primary key, b int,c integer);
create table tab1136(a json,b int,c integer,foreign key(a) references  tab1136(a));

--清理数据
drop table if exists tab1131 cascade;
drop table if exists tab1132 cascade;
drop table if exists tab1133 cascade;
drop table if exists tab1134 cascade;
drop table if exists tab1135 cascade;
drop table if exists tab1136 cascade;