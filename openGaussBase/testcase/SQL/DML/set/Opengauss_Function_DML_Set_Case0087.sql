--  @testpoint:约束默认是no deferable的，SET CONSTRAINTS 语句，添加参数all（主键约束和唯一约束）
--建表同时定义主键约束和唯一约束
drop table if exists t4;
create table t4 (id int primary key,name varchar(40) unique);
--插入数据
--查看约束名字
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--开启事务
start transaction;
--设置当前事务检查行为的约束条件为DEFERRED
SET CONSTRAINTS all DEFERRED;
--修改数据，合理报错（即使设置了constraints为deferred，由于建表时约束为no deferred的，也是就约束是不能延迟的检查，执行时，即使设置constraints为deferred时，也不生效）
update t4 set id=id+1;
--关闭事务
end;

--开启事务
start transaction;
--设置约束检查条件为IMMEDIATE
SET CONSTRAINTS t4_pkey IMMEDIATE;
--修改数据，合理报错（约束在每条语句后进行检查）
 update t4 set id=id+1;
--关闭事务
end;
--删表
drop table t4;