-- @testpoint: 视图所有者删除视图，成功,不加cascade，合理报错
--建表
drop table if exists table_view_030;
create table table_view_030(id int,name varchar(20));
--插入数据
insert into table_view_030 values(1,'hello'),(2,'world');
--创建视图
drop view if exists temp_view_030 cascade;
create view temp_view_030 as select * from table_view_030;
--删除视图
drop view temp_view_030;
--删除不存在的视图,添加if exists
drop view if exists temp_view_030;
--删表
drop table table_view_030;
--删除表，不加cascade，合理报错
drop table table_view_030;
--删除表，添加restrict，合理报错
drop table table_view_030 restrict;
