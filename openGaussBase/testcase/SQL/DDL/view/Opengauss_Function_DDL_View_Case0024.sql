-- @testpoint: 取消列视图列的默认值,if exists选项测试，省略if exists，视图名不存在，合理报错
--建表
drop table if exists table_view_024;
create table table_view_024(id int,name varchar(20));
--插入数据
insert into table_view_024 values(1,'hello'),(2,'world');
--创建视图
drop view if exists temp_view_024 cascade;
create view temp_view_024 as select * from table_view_024;
--给视图id列设置默认值
alter view if exists temp_view_024 alter column id set default 5;
--取消默认值，视图名不存在，不报错
--取消默认值，视图名不存在，合理报错
--删表
drop table table_view_024 cascade;