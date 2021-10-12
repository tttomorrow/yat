-- @testpoint: 重置视图的选项
--建表
drop table if exists table_view_029;
create table table_view_029(id int,name varchar(20));
--插入数据
insert into table_view_029 values(1,'hello'),(2,'world');
--创建视图
drop view if exists temp_view_029 cascade;
create view temp_view_029 as select * from table_view_029;
--设置视图选项
alter view if exists temp_view_029 set (security_barrier = true);
--重置视图选项
alter view if exists temp_view_029 reset (security_barrier );
--删表
drop table table_view_029 cascade;