-- @testpoint: 修改数据，使用目标表的别名加字段名来引用这个字段
--建表
drop table if exists t_update01;
create table t_update01(id int,name varchar(10));
--插入数据
insert into t_update01 values(1,'hello'),(2,'world'),(3,'hello1');
--修改数据,修改3条数据
update t_update01 as t set t.id = id + 1;
update t_update01 as t set t.name = upper(name);
--查询
select * from t_update01;
--删表
drop table t_update01;