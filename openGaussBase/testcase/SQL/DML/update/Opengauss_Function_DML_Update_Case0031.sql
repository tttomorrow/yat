-- @testpoint: update表的数据，添加*，成功
--建表
drop table if exists t_update01;
create table t_update01(id int,name varchar(10));
--插入数据
insert into t_update01 values(1,'hello'),(2,'world'),(3,'hello1');
--修改数据
update t_update01 * set id = id + 1;
update t_update01 * as t set t.name = upper(name);
--查询
select * from t_update01;
--删表
drop table t_update01;