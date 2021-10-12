-- @testpoint: 设置视图的选项,非法选项，合理报错
--建表
drop table if exists table_view_028;
create table table_view_028(id int,name varchar(20));
--插入数据
insert into table_view_028 values(1,'hello'),(2,'world');
--创建视图
drop view if exists temp_view_028 cascade;
create view temp_view_028 as select * from table_view_028;
--设置视图选项，报错
alter view temp_view_028 set (security435_barrier = true);
alter view temp_view_028 set (参数security_barrier = false);
--删表
drop table table_view_028 cascade;