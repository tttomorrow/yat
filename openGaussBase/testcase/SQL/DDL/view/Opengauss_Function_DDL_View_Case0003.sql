-- @testpoint: 对视图进行dml操作，合理报错
--建表
drop table if exists table_view_003;
create table table_view_003(id int,name varchar(20));
--插入数据
insert into table_view_003 values(1,'hello'),(2,'world');
insert into table_view_003 values(2344,'数据库'),(2,'测试');
--查询
select * from table_view_003;
--创建视图
create or replace view temp_view_003 as select * from table_view_003;
--给视图插入数据，合理报错
insert into temp_view_003 values(123,'hello');
--修改视图数据，合理报错
update temp_view_003 set id = id +2 where name = 'hello';
--删除视图数据，合理报错
delete from temp_view_003;
--删表
drop table table_view_003 cascade;