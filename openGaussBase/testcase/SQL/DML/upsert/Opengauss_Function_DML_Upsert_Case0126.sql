-- @testpoint: upsert子查询列与目标更新列数据类型及非空约束校验，不符合要求，合理报错

--创建upeset及子查询表，插入数据
drop table if exists t_dml_upsert_sub0126;
create table t_dml_upsert_sub0126 (a int,b text,c text);
insert into t_dml_upsert_sub0126 values(generate_series(1,10),generate_series(1,10),'c-'||generate_series(1,10));
drop table if exists t_dml_upsert0126;
create table t_dml_upsert0126 (a int primary key, b int unique, c int not null, d text);
insert into t_dml_upsert0126 values (1,1,1),(2,2,2),(3,3,3),(4,4,4);
select * from t_dml_upsert0126;
--目标列为int类型，子查询结果为text类型，无法隐式转换为int类型，合理报错
insert into t_dml_upsert0126 values(1,5,3) on duplicate key update c = (select c from t_dml_upsert_sub0126 where a = excluded.a);
--目标列为int类型，子查询结果为text类型，可以隐式转换为int类型，insert成功
insert into t_dml_upsert0126 values(2,5,0) on duplicate key update c = (select b from t_dml_upsert_sub0126 where a = excluded.a*3);
select * from t_dml_upsert0126;
--目标列为text类型，子查询结果为text类型，insert成功
insert into t_dml_upsert0126 values(3,2,1) on duplicate key update d = (select c from t_dml_upsert_sub0126 where a = excluded.a*3);
select * from t_dml_upsert0126;
--目标列为not null，子查询结果为空，合理报错
insert into t_dml_upsert0126 values(1,5,1) on duplicate key update c = (select c from t_dml_upsert_sub0126 where a>10);
--目标列为unique，子查询结果与存量数据重复，合理报错
insert into t_dml_upsert0126 values(1,5,1) on duplicate key update b = (select b from t_dml_upsert_sub0126 where a=2);
--处理测试数据
drop table if exists t_dml_upsert0126;
drop table if exists t_dml_upsert_sub0126;