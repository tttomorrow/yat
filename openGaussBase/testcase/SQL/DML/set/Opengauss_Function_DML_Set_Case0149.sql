--  @testpoint:使用SET CONSTRAINTS命令，设置约束名列表为可推迟
--建表
drop table if exists t4;
create table t4 (id int primary key,name varchar(40) unique);
--插入数据
insert into t4 values(1,'z'),(2,'bj');
--查看约束名
select conname,condeferrable,condeferred from pg_constraint where conrelid = (select oid from pg_class where relname='t4');
--开启事务
start transaction;
--SET CONSTRAINTS命令，设置约束名列表为可推迟,合理报错
SET CONSTRAINTS t4_pkey,t4_name_key DEFERRED;
end;
--删表
drop table t4;




