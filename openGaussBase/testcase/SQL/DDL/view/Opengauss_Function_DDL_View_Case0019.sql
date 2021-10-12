-- @testpoint: 修改不存在的视图所属模式，添加if exists选项，不会报错
--建表
drop table if exists table_view_019;
create table table_view_019(id int,name varchar(20));
--插入数据
insert into table_view_019 values(1,'hello'),(2,'world');
--创建模式
drop schema if exists schema_view_019;
create schema schema_view_019;
--创建视图
drop view if exists temp_view_019 cascade;
create view temp_view_019 as select * from table_view_019;
--修改视图所属模式,添加if exists选项，视图名不存在
--通过系统表查询视图信息，模式不变
select schemaname,viewname from pg_views where viewname = 'temp_view_019';
--删除表
drop table table_view_019 cascade;
--删除模式
drop schema schema_view_019;