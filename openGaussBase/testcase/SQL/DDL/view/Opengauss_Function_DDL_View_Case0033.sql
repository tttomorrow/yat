-- @testpoint: 视图有依赖对象，删除依赖对象不加cascade，合理报错
--建表
drop table if exists table_view_033 cascade;
create table table_view_033(id int,job_title varchar(20));
--插入数据
insert into table_view_033 values(1,'engineer'),(2,'sales representative');
--创建视图
drop view if exists temp_view_033 cascade;
create view temp_view_033 as select * from table_view_033 where job_title = 'sales representative';
--查询视图
select * from temp_view_033;
--基于temp_view_033视图创建另一个名为temp_view_033_bak的视图
create or replace view temp_view_033_bak as select * from temp_view_033;
--查询视图
select * from temp_view_033_bak;
--删除temp_view_033视图,不加cascade，合理报错
drop view temp_view_033;
--删除temp_view_033视图,添加restrict，合理报错
drop view temp_view_033 restrict;
--删除temp_view_033视图,添加cascade，删除成功
drop view temp_view_033 cascade;
--删表
drop table table_view_033 cascade;