--  @testpoint:SET CONSTRAINTS语句，指定约束名不存在，合理报错
--建表
drop table if exists t4;
create table t4 (id int unique DEFERRABLE,name varchar(40));
--查看约束名字
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--开启事务
 start transaction;
 --设置约束检查条件为IMMEDIATE（约束名不存在）
 SET CONSTRAINTS t4_id_key1 IMMEDIATE;
 --结束事务
 end;
 --删表
 drop table t4;