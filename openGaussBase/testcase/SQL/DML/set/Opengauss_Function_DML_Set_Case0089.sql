-- @testpoint: 使用SET CONSTRAINTS语句，设置多个约束名,部分step合理报错
--建表同时定义检查约束和主键约束
drop table if exists t4;
create table t4 (id int check (id >5),name varchar(40) primary key);
insert into t4 values(6,'a'),(7,'b');
--查看约束名字
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--开启事务
start transaction;
--设置当前事务检查行为的约束条件，合理报错（默认是不能推迟的，即NOT DEFERRABLE不能用set命令改变）
SET CONSTRAINTS t4_id_check,t4_pkey DEFERRED;
--关闭事务
end;
--开启事务
start transaction;
--设置当前事务检查行为的约束条件,立即检查
SET CONSTRAINTS t4_id_check,t4_pkey immediate;
--修改数据，合理报错（违反检查约束)
update t4 set id =id -2;
--关闭事务
end;
drop table t4;
