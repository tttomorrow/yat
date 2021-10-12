-- @testpoint: 插入数据,使用insert..returning子句,指定字段的输出名称
--建表
drop table if exists t_insert02;
create table t_insert02(id int,name varchar(10));
--插入数据成功
insert into t_insert02 values (2,'小xiao明') returning id as new_id;
insert into t_insert02 values (2,'小名明') returning id,name as new_name;
--删表
drop table if exists t_insert02;

