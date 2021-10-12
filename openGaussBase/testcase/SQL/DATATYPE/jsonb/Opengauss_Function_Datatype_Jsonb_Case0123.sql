-- @testpoint: 临时表（local）使用数据类型为jsonb的列创建主外键，合理报错

--创建临时表创建主键
drop table if exists tab1231;
create local temporary table tab1231(id int,name varchar,message jsonb primary key);
drop table if exists tab1232;
create local temporary table tab1232(id int,name varchar,message jsonb, primary key(message));

--创建临时表创建外键:jsonb类型的列不为主键
drop table if exists tab1233;
drop table if exists tab1234;
create local temporary table tab1233(a int primary key, b jsonb,c integer);
create local temporary table tab1234(a int, b jsonb,c integer,  foreign key(a) references  tab1233(a));

--创建临时表创建外键:jsonb类型的列为主键
drop table if exists tab1235;
drop table if exists tab1236;
create local temporary table tab1235(a jsonb primary key, b int,c integer);
create local temporary table tab1236(a jsonb  primary key,b int,c integer,foreign key(a) references  tab1236(a));

--jsonb类型的列创建唯一约束，并创建外键
drop table if exists tab1237;
drop table if exists tab1238;
drop table if exists tab1239;
create local temporary table tab1237(a int,b jsonb unique,c integer,foreign key(b) references  tab1236(a));
create local temporary table tab1238(a jsonb,b jsonb unique,c integer,foreign key(b) references  tab1237(b));

--jsonb类型的列无唯一约束或主键：合理报错
drop table if exists tab1239;
create local temporary table tab1239(a int primary key, b jsonb,c integer,foreign key(a) references  tab1234(a));

--清理数据
drop table if exists tab1231 cascade;
drop table if exists tab1232 cascade;
drop table if exists tab1233 cascade;
drop table if exists tab1234 cascade;
drop table if exists tab1235 cascade;
drop table if exists tab1236 cascade;
drop table if exists tab1237 cascade;
drop table if exists tab1238 cascade;
drop table if exists tab1239 cascade;