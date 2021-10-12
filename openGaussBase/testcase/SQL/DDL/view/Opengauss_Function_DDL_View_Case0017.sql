-- @testpoint: 修改视图所属模式,用户没有新模式的CREATE权限
--建表
drop table if exists table_view_017;
create table table_view_017(id int,name varchar(20));
insert into table_view_017 values(1,'hello'),(2,'world');
--创建模式
drop schema if exists schema_view_017;
create schema schema_view_017;
--创建视图
drop view if exists temp_view_017 cascade;
CREATE VIEW temp_view_017 AS SELECT * from table_view_017;
--回收模式上的CREATE权限
revoke create on schema schema_view_017 from public;
--修改视图所属模式
ALTER VIEW temp_view_017 SET SCHEMA schema_view_017;
--通过系统表查询视图信息
select schemaname,viewname from pg_views where viewname = 'temp_view_017';
--删除表
drop table table_view_017 cascade;
--删除模式
drop schema schema_view_017;