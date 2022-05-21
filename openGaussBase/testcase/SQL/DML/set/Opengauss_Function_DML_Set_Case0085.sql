-- @testpoint: 约束默认是no deferable的，使用SET CONSTRAINTS语句设置当前事务检查行为的约束条件（检查约束）,部分step合理报错
--建表同时定义检查约束
drop table if exists t4;
create table t4 (id int check (id >5),name varchar(40));
--查看约束名字
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--开启事务
start transaction;
--设置当前事务检查行为的约束条件，合理报错（默认是不能推迟的，即NOT DEFERRABLE不能用set命令改变）
SET CONSTRAINTS t4_id_check DEFERRED;
--关闭事务
end;

--插入数据
insert into t4 values(6,'tom'),(7,'lily');
--开启事务
start transaction;
--设置约束检查条件为IMMEDIATE
SET CONSTRAINTS t4_id_check IMMEDIATE;
--修改数据，合理报错（约束在每条语句后进行检查）
 update t4 set id=id-2;

 --关闭事务
end;
--查询表数据
select * from t4;
--删表
drop table t4;
