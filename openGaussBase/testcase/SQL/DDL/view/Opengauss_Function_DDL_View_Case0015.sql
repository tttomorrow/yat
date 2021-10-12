-- @testpoint: 视图所有者修改视图名称，成功
--建表并插入数据
drop table if exists table_view_015;
create table table_view_015(id int,name varchar(20));
insert into table_view_015 values(1,'hello'),(2,'world');
--创建视图
create or replace view temp_view_015 as select * from table_view_015;
--修改视图名称
alter view temp_view_015 rename to temp_view_015_new;
--删表
drop table table_view_015 cascade;