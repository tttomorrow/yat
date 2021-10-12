-- @testpoint: 修改数据，子查询中使用group by..having子句
--建表
drop table if exists t_update003;
create table t_update003(c_x varchar(20), c_y int );
--插入数据
insert into t_update003 values('a',3);
insert into t_update003 values('c',2);
insert into t_update003 values('b',5);
insert into t_update003 values('a',1);
--修改数据
update t_update003  set (c_x,c_y) = (SELECT c_x, sum(c_y) FROM t_update003 GROUP BY c_x HAVING sum(c_y) > 4);
--查询
select * from t_update003;
--删表
drop table t_update003;