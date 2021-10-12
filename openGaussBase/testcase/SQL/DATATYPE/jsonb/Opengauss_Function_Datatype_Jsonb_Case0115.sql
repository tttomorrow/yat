-- @testpoint: json类型的临时创建主键:不支持，合理报错

--在本地临时表上建主键：不支持
drop table if exists tab111 cascade;
create local temporary table tab111(id int,name varchar,message json primary key);

--在全局临时表上建主键：不支持
drop table if exists tab1112 cascade;
create global temporary table tab1112(id int,name varchar,message json primary key);

--清理数据
drop table if exists tab111 cascade;
drop table if exists tab1112 cascade;
