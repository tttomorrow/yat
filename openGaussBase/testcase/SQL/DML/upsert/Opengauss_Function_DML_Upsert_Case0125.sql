-- @testpoint: upsert子查询结果行列限制及语法格式限制，不符合要求，合理报错

--创建upeset及子查询表，插入数据
drop table if exists t_dml_upsert_sub0125;
create table t_dml_upsert_sub0125 (a int,b text,c text);
insert into t_dml_upsert_sub0125 values(generate_series(1,10),'b-'||generate_series(1,10),'c-'||generate_series(1,10));
drop table if exists t_dml_upsert_sub0125_01;
create table t_dml_upsert_sub0125_01 (a int);
insert into t_dml_upsert_sub0125_01 values(generate_series(1,10));
drop table if exists t_dml_upsert0125;
create table t_dml_upsert0125 (a int primary key, b text, c text, d text);
insert into t_dml_upsert0125 values (1,1,1),(2,2,2),(3,3,3),(4,4,4);
--子查询没有用()引用
insert into t_dml_upsert0125 values(3,5) on duplicate key update (b,c,d) = select t.a,t.b,t.c from t_dml_upsert_sub0125 t where t.a= excluded.a;
--子查询结果行数大于1，报错ERROR
insert into t_dml_upsert0125 values(2,5) on duplicate key update (c,b) = (select b,c from t_dml_upsert_sub0125 where a > excluded.a);
select * from t_dml_upsert0125;
--子查询结果行数等于1，插入成功
insert into t_dml_upsert0125 values(2) on duplicate key update (b,c) = (select b,c from t_dml_upsert_sub0125 where a = excluded.a);
select * from t_dml_upsert0125;
--子查询结果行数等于0
insert into t_dml_upsert0125 values(1,11) on duplicate key update b = (select a from t_dml_upsert_sub0125 where a > excluded.b);
select * from t_dml_upsert0125;
--子查询返回列数小于目标列数，报错ERROR
insert into t_dml_upsert0125 values(2,5) on duplicate key update (b,c) = (select a from t_dml_upsert_sub0125 where a = excluded.a);
--子查询返回列数大于目标列数，报错ERROR
insert into t_dml_upsert0125 values(2,5) on duplicate key update (b,c) = (select a,b,c from t_dml_upsert_sub0125 where a = excluded.a);
--子查询返回列数等于目标列数，插入成功
insert into t_dml_upsert0125 values(2,5) on duplicate key update (b,c,d) = (select a,b,c from t_dml_upsert_sub0125 where a= excluded.a);
select * from t_dml_upsert0125;
insert into t_dml_upsert0125 values(3,5) on duplicate key update (b,c,d) = (select t.a,t.b,t.c from t_dml_upsert_sub0125 t where t.a= excluded.a);
select * from t_dml_upsert0125;
explain (costs off, verbose) insert into t_dml_upsert0125 values(3,5) on duplicate key update (b,c,d) = (select t.a,t.b,t.c from t_dml_upsert_sub0125 t where t.a= excluded.a);
--muilt-set子查询返回列为*，与目标列数相等，报错（必须对应到具体列）
insert into t_dml_upsert0125 values(2,5) on duplicate key update (b,c,d) = (select * from t_dml_upsert_sub0125 where a= excluded.a);
--single-set子查询返回列为*，与目标列数相等,插入成功
insert into t_dml_upsert0125 values(2,2) on duplicate key update b = (select * from t_dml_upsert_sub0125_01 where a= excluded.b*2);
select * from t_dml_upsert0125;
--处理测试数据
drop table if exists t_dml_upsert0125;
drop table if exists t_dml_upsert_sub0125;
drop table if exists t_dml_upsert_sub0125_01;