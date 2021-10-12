--  @testpoint:约束默认是no deferable的，使用SET CONSTRAINTS语句设置当前事务检查行为的约束条件（唯一约束）
--建表同时定义主键约束
drop table if exists t4;
create table t4 (id int unique,name varchar(40));
--查看约束名字
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--开启事务
start transaction;
--设置当前事务检查行为的约束条件，合理报错（默认是不能推迟的，即NOT DEFERRABLE不能用set命令改变）
SET CONSTRAINTS t4_id_key DEFERRED;

--关闭事务
end;
--开启事务
start transaction;
--设置约束检查条件为IMMEDIATE
SET CONSTRAINTS t4_id_key IMMEDIATE;
--插入数据
insert into t4 values(1,'tom'),(2,'lily');
--修改数据，合理报错（约束在每条语句后进行检查）
 update t4 set id=id+1;
 --关闭事务
end;
--删表
drop table t4;
