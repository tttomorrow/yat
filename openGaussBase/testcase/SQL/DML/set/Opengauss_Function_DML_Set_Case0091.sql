--  @testpoint:约束建成deferable，事务块外，执行SET CONSTRAINTS不生效（主键约束和唯一约束）
--建表
drop table if exists t4;
create table t4 (id int primary key DEFERRABLE,name varchar(40) unique DEFERRABLE);
--查看约束名字
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--插入数据
insert into t4 values(1,'1111111111111111');
insert into t4 values(2,'2222222222222222');
--修改数据，成功
update t4 set id=id+1;
select * from t4;

 --设置约束检查条件为IMMEDIATE
 SET CONSTRAINTS all IMMEDIATE;
 --修改数据,合理报错（立即检查）
 update t4 set id=3 where name='1111111111111111';
 update t4 set name='2222222222222222' where id=2;


truncate table t4;
 --插入数据
insert into t4 values(1,'1111111111111111');
insert into t4 values(2,'2222222222222222');

 --设置约束检查条件为DEFERRED
 SET CONSTRAINTS all DEFERRED;
 --修改数据（合理报错，事务外设置延迟检查约束，不生效）
 update t4 set id=2 where id=1;
 select * from t4;
 --删表
 drop table t4;