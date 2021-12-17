--  @testpoint:约束建成deferable，使用SET CONSTRAINTS语句设置当前事务检查行为的约束条件（唯一约束）
--建表
drop table if exists t4;
create table t4 (id int unique DEFERRABLE,name varchar(40));
--查看约束名字
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--插入数据
insert into t4 values(1,'1111111111111111');
insert into t4 values(2,'2222222222222222');
--修改数据，成功
update t4 set id=id+1;
select * from t4;
--开启事务
 start transaction;
 --设置约束检查条件为IMMEDIATE
 SET CONSTRAINTS t4_id_key IMMEDIATE;
 --修改数据,合理报错（立即检查）
 update t4 set id=3 where name='1111111111111111';
 --结束事务
 end;

truncate table t4;
 --插入数据
insert into t4 values(1,'1111111111111111');
insert into t4 values(2,'2222222222222222');
--开启事务
 start transaction;
 --设置约束检查条件为DEFERRED
 SET CONSTRAINTS t4_id_key DEFERRED;
 --修改数据,修改成功
 update t4 set id=2 where id=1;
 select * from t4;
 --结束事务(提交时，才检查约束，合理报错，主键冲突)
 end;
 --数据回到未更新前
 select * from t4;
 --删表
 drop table t4;