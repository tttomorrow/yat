-- @testpoint: 行存表使用数据类型为jsonb的列创建主外键，合理报错

--创建行存表创建主键
drop table if exists tab1201;
create table tab1201(id int,name varchar,message jsonb primary key);
drop table if exists tab1202;
create table tab1202(id int,name varchar,message jsonb, primary key(message));

--创建行存表创建外键:jsonb类型的列不为主键
drop table if exists tab1203;
drop table if exists tab1204;
create table tab1203(a int primary key, b jsonb,c integer);
create table tab1204(a int, b jsonb,c integer,  foreign key(a) references  tab1203(a));

--创建行存表创建外键:jsonb类型的列为主键
drop table if exists tab1205;
drop table if exists tab1206;
create table tab1205(a jsonb primary key, b int,c integer);
create table tab1206(a jsonb  primary key,b int,c integer,foreign key(a) references  tab1206(a));

--jsonb类型的列创建唯一约束，并创建外键
drop table if exists tab1207;
drop table if exists tab1208;
drop table if exists tab1209;
create table tab1207(a int,b jsonb unique,c integer,foreign key(b) references  tab1206(a));
create table tab1208(a jsonb,b jsonb unique,c integer,foreign key(b) references  tab1207(b));

--jsonb类型的列无唯一约束或主键：合理报错
drop table if exists tab1209;
create table tab1209(a int primary key, b jsonb,c integer,foreign key(a) references  tab1204(a));

--清理数据
drop table if exists tab1201 cascade;
drop table if exists tab1202 cascade;
drop table if exists tab1203 cascade;
drop table if exists tab1204 cascade;
drop table if exists tab1205 cascade;
drop table if exists tab1206 cascade;
drop table if exists tab1207 cascade;
drop table if exists tab1208 cascade;
drop table if exists tab1209 cascade;