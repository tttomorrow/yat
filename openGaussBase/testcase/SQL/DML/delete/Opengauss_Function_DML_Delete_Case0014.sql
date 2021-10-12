--  @testpoint:删除表数据，where后子句不满足条件，删除0行
drop table if exists t_delete03;
create table t_delete03(id int,name varchar(10));
--插入数据
insert into t_delete03 values (1,'小明');
insert into t_delete03 values (2,'小李');
--删除0行
delete from t_delete03 where id < 1;
--删除表
drop table t_delete03;