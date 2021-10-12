-- @testpoint: 创建视图,视图名符合标识符命名规范
--建表
drop table if exists table_view_007;
create table table_view_007(id int,name varchar(20));
--插入数据
insert into table_view_007 values(1,'hello'),(2,'world');
insert into table_view_007 values(2344,'数据库'),(2,'测试');
--查询
select * from table_view_007;
--创建视图，视图名由由为字母、下划线、数字（0-9）或美元符号（$）组成
drop view if exists t_delete01$ cascade;
create view t_delete01$ as select * from table_view_007;
--查询
select * from t_delete01$;
--创建视图，视图名以_开头
 create or replace view _delete01$ as select * from table_view_007;
--创建视图，视图名以大写字母开头
 create or replace view t_delete01$ as select * from table_view_007;
 --创建视图，视图名以大写字母开头且添加双引号
 create or replace view "t_delete01$" as select * from table_view_007;
 --删表
 drop table table_view_007 cascade;