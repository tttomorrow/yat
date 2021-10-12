-- @testpoint: 创建视图,视图名不符合标识符命名规范，合理报错
--建表
drop table if exists table_view_008;
create table table_view_008(id int,name varchar(20));
--插入数据
insert into table_view_008 values(1,'hello'),(2,'world');
insert into table_view_008 values(2344,'数据库'),(2,'测试');
--创建视图，视图名已数字开头
drop view if exists t_delete01$ cascade;
create view 1_delete01$ as select * from table_view_008;
--创建视图，视图名已()开头
 create or replace view ()_delete01$ as select * from table_view_008;
  --删表
 drop table table_view_008 cascade;

