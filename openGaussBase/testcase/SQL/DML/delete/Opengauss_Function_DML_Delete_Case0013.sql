--  @testpoint:delete语句中，添加with_query语句,子查询是SELECT
--建表
drop table if exists t_delete03;
create table t_delete03(id int,name varchar(10));
--插入数据
insert into t_delete03 values (1,'小明');
insert into t_delete03 values (2,'小李');
--先通过子查询得到一张临时表tmp_delete03，然后删除表t_delete03中的数据
with tmp_delete03 as(select * from t_delete03) delete from t_delete03 returning id;
with tmp_delete03 as(select * from t_delete03) delete from t_delete03 returning *;
--删除表
drop table t_delete03;



