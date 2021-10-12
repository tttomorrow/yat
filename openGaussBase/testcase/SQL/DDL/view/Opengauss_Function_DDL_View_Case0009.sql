-- @testpoint: 创建视图,添加视图的字段名
--建表
drop table if exists table_view_009;
create table table_view_009(id int,name varchar(20));
--插入数据
insert into table_view_009 values(1,'he&*%&%llo'),(2,'world');
--创建视图
drop view if exists temp_view_009;
create view temp_view_009(id) as select * from table_view_009;
--替换已有视图，添加字段名
create or replace view temp_view_009(id,name) as select * from table_view_009;
--查询视图
select * from temp_view_009;
--删表
drop table table_view_009 cascade;