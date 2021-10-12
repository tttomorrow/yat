--  @testpoint:列存表，使用returnng子句，合理报错
--创建列存表
drop table if exists t_delete03;
create table t_delete03(id int,name varchar(10))with(orientation= column);
--插入数据
insert into t_delete03 values (1,'小明');
insert into t_delete03 values (2,'小李');
--使用delete...returning语句，合理报错
delete from t_delete03 where id =2 returning id;
delete from t_delete03 where id =2 returning *;
--删除表
drop table t_delete03;