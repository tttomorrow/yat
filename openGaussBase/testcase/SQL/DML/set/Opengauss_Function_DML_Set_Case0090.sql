--  @testpoint:使用SET CONSTRAINTS语句，设置无效检查约束，合理报错
--建表同时定义检查约束
drop table if exists t4;
create table t4 (id int check (id >5),name varchar(40));
--查看约束名字
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--开启事务
start transaction;
--设置当前事务检查行为的约束条件，合理报错
SET CONSTRAINTS t4_id_check DEFERRABLE;
SET CONSTRAINTS t4_id_check immediately;
--关闭事务
end;
--删表
drop table t4;