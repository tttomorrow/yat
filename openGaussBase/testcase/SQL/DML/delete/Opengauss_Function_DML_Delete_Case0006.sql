--  @testpoint:delete..returning子句测试
--建表
drop table if exists t_delete03;
create table t_delete03(id int,name varchar(10));
--插入数据
insert into t_delete03 values (1,'小明');
insert into t_delete03 values (2,'小李');
--删除表数据，returning所有字段，删除1条数据
delete from t_delete03 where id =1 returning *;
--删除表数据，returning所有字段，删除0条数据
delete from t_delete03 where id =1 returning id,name;
--删除表数据，returning id字段，删除1条数据
delete from t_delete03 where id =2 returning id;
--删除表数据，returning output_name,删除0条数据
delete from t_delete03 where id =2 returning id as id_del;
--删除表数据，returning output_name,省略as，删除0条数据
delete from t_delete03 where id =2 returning id id_del;
--删除表
drop table t_delete03;