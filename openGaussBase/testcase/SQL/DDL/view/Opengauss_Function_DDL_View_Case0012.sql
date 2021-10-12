-- @testpoint: 创建视图后，修改表数据，查询视图信息，同步更新
--建表
drop table if exists table_view_012;
create table table_view_012(id int,name varchar(20));
--插入数据
insert into table_view_012 values(1,'hello'),(2,'world');
insert into table_view_012 values(2344,'数据库'),(2,'测试');
--创建视图
drop view if exists temp_view_012 cascade;
create temp view temp_view_012 as select * from table_view_012;
--查询视图
select * from temp_view_012;
--修改表数据
update table_view_012 set id = id + 1 where name = 'hello';
--查询视图，name为'hello'的id值更新为2
select * from temp_view_012;
--删表
drop table table_view_012 cascade;
