-- @testpoint: 临时表（global）使用数据类型为jsonb的列创建主外键，合理报错

--创建临时表创建主键
drop table if exists tab1241;
create global temporary table tab1241(id int,name varchar,message jsonb primary key);
drop table if exists tab1242;
create global temporary table tab1242(id int,name varchar,message jsonb, primary key(message));

--创建临时表创建外键:jsonb类型的列不为主键
drop table if exists tab1243;
drop table if exists tab1244;
create global temporary table tab1243(a int primary key, b jsonb,c integer);
create global temporary table tab1244(a int, b jsonb,c integer,  foreign key(a) references  tab1243(a));

--创建临时表创建外键:jsonb类型的列为主键
drop table if exists tab1245;
drop table if exists tab1246;
create global temporary table tab1245(a jsonb primary key, b int,c integer);
create global temporary table tab1246(a jsonb  primary key,b int,c integer,foreign key(a) references  tab1246(a));

--jsonb类型的列创建唯一约束，并创建外键
drop table if exists tab1247;
drop table if exists tab1248;
drop table if exists tab1249;
create global temporary table tab1247(a int,b jsonb unique,c integer,foreign key(b) references  tab1246(a));
create global temporary table tab1248(a jsonb,b jsonb unique,c integer,foreign key(b) references  tab1247(b));

--jsonb类型的列无唯一约束或主键：合理报错
drop table if exists tab1249;
create global temporary table tab1249(a int primary key, b jsonb,c integer,foreign key(a) references  tab1244(a));

--清理数据
drop table if exists tab1241 cascade;
drop table if exists tab1242 cascade;
drop table if exists tab1243 cascade;
drop table if exists tab1244 cascade;
drop table if exists tab1245 cascade;
drop table if exists tab1246 cascade;
drop table if exists tab1247 cascade;
drop table if exists tab1248 cascade;
drop table if exists tab1249 cascade;