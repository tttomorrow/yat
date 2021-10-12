--  @testpoint:多表之间，使用using子句
--创建表1
drop table if exists t_delete03;
create table t_delete03(id int,name varchar(10));
--插入数据
insert into t_delete03 values (1,'小明');
insert into t_delete03 values (2,'小李');
--创建表2
drop table if exists t_delete04;
create table t_delete04(id int,t_num varchar(10));
--插入数据
insert into t_delete04 values (1,'小明');
insert into t_delete04 values (2,'小李');
--两个表联合删除，删除t_03表1条数据
DELETE FROM t_delete03 t_03 USING t_delete04 t_04 WHERE t_03.id = t_04.id AND t_03.id = 1;
--删除表
drop table t_delete03;
drop table t_delete04;