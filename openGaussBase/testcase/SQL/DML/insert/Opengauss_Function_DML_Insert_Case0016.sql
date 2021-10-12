-- @testpoint: 插入数据,使用insert..returning子句
--建表
drop table if exists t_insert02;
create table t_insert02(id int,name varchar(10));
--插入数据成功，返回实际插入的行
insert into t_insert02 values (2,'小明') returning *;
--返回id行
insert into t_insert02 values (3,'小明') returning id;
--返回id和name行等价于*
insert into t_insert02 values (4,'小明') returning id,name;
--删表
drop table if exists t_insert02;

