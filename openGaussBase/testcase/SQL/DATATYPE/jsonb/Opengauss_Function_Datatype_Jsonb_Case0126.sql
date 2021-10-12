-- @testpoint: 数据类型jsonb修改为其他数据类型,不支持直接转化，合理报错

--创建数据类型为jsonb的表,修改表的数据类型jsonb为其他数据类型
--char(100)
drop table if exists tab1261;
create table tab1261(id int,name varchar,message jsonb);
insert into tab1261 values(023,'Jack','{"age":20,"city":"xiamen"}');
alter table tab1261 alter column message type char(100) USING message::char(100);
drop table if exists tab1261;

--varchar(100)
drop table if exists tab1262;
create table tab1262(id int,name varchar,message jsonb);
insert into tab1262 values(001,'Jane','{"age":18,"city":"xianyang"}');
alter table tab1262 modify (message varchar(100));
drop table if exists tab1262;

--text
drop table if exists tab1263;
create table tab1263(id int,name varchar,message jsonb);
insert into tab1263 values(012,'Joy','{"age":19,"city":"qingdao"}');
alter table tab1263 modify (message varchar(100));
drop table if exists tab1263;

--int
drop table if exists tab1264;
create table tab1264(id int,name varchar,message jsonb);
insert into tab1264 values(035,'Jim','{"age":21,"city":"shanghai"}');
alter table tab1264 modify (message int);
drop table if exists tab1264;