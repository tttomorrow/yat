-- @testpoint: 设置视图列的默认值
--建表
drop table if exists table_view_016;
create table table_view_016(id int,name varchar(20));
--插入数据
insert into table_view_016 values(1,'hello'),(2,'world');
--创建视图
drop view if exists temp_view_016 cascade;
create view temp_view_016 as select * from table_view_016;
--给视图id列设置默认值
alter view if exists temp_view_016 alter column id set default 5;
--清理环境
drop table if exists table_view_016 cascade;