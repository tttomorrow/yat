-- @testpoint: 创建视图，使用or replace替换已有视图
--建表
drop table if exists table_view_004;
create table table_view_004(id int,name varchar(20));
--创建视图
drop view if exists temp_view_004 cascade;
create view temp_view_004 as select * from table_view_004;
--查询视图，无数据
select * from temp_view_004;
--插入数据
insert into table_view_004 values(1,'hello'),(2,'world');
insert into table_view_004 values(2344,'数据库'),(2,'测试');
--创建视图，添加or replace选项,视图名存在，创建成功
create or replace view temp_view_004 as select * from table_view_004;
--查询视图，4条数据
select * from temp_view_004;
--删除视图
drop view temp_view_004;
--删表
drop table table_view_004;