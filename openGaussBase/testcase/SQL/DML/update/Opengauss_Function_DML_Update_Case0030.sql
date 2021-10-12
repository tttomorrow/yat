-- @testpoint: 修改数据，设置新值为default
--建表1
drop table if exists t_update01;
create table t_update01(id int,name varchar(10));
--插入数据
insert into t_update01 values(1,'hello'),(2,'world'),(3,'hello1');
--修改数据,修改id列3条数据为空值
update t_update01 set id = default;
--查询
select * from t_update01;
--建表2，id列指定默认值
drop table if exists t_update02;
create table t_update02(id int default 10,name varchar(10));
--插入数据
insert into t_update02 values(1,'hello'),(2,'world'),(3,'hello1');
--修改id列的值均为default
update t_update02 set id = default;
--查询，id列均为10
select * from t_update01;
--删表
drop table t_update01;
drop table t_update02;