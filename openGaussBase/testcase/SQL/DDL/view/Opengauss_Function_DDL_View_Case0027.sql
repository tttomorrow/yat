-- @testpoint: 设置视图的选项
--建表
drop table if exists table_view_027;
create table table_view_027(id int,name varchar(20));
--插入数据
insert into table_view_027 values(1,'hello'),(2,'world');
--创建视图
drop view if exists temp_view_027 cascade;
create view temp_view_027 as select * from table_view_027;
--设置视图选项
alter view if exists temp_view_027 set (security_barrier = true);
alter view if exists temp_view_027 set (security_barrier = false);
--删表
drop table table_view_027 cascade;