--  @testpoint:事务中，使用delete子句
--建表
drop table if exists t_delete03;
create table t_delete03(id int,name varchar(10));
--插入数据
insert into t_delete03 values (1,'小明');
insert into t_delete03 values (2,'小李');
--开启事务
start transaction;
--删除表数据
delete from t_delete03;
--回滚
rollback;
--查询表信息，表数据恢复
select * from t_delete03;
--删除表
drop table t_delete03;