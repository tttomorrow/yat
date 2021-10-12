-- @testpoint: 修改已存在的视图所属模式，添加if exists选项，修改成功
--建表
drop table if exists table_view_018;
create table table_view_018(id int,name varchar(20));
--插入数据
insert into table_view_018 values(1,'hello'),(2,'world');
insert into table_view_018 values(2344,'数据库'),(2,'测试');
--创建模式
drop schema if exists schema_view_018;
create schema schema_view_018;
--创建视图
drop view if exists temp_view_018 cascade;
create view temp_view_018 as select * from table_view_018;
--修改视图所属模式,添加if exists选项
alter view if exists temp_view_018 set schema schema_view_018;
--通过系统表查询视图信息
select schemaname,viewname from pg_views where viewname = 'temp_view_018';
--删除表
drop table table_view_018 cascade;
--删除模式
drop schema schema_view_018;