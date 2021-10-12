-- @testpoint: 取消列视图列的默认值
--建表
drop table if exists table_view_023;
create table table_view_023(id int,name varchar(20));
--插入数据
insert into table_view_023 values(1,'hello'),(2,'world');
--创建视图
drop view if exists temp_view_023 cascade;
create view temp_view_023 as select * from table_view_023;
--给视图id列设置默认值
alter view if exists temp_view_023 alter column id set default 5;
--取消默认值
alter view if exists temp_view_023 alter column id drop default;
--删表
drop table table_view_023 cascade;