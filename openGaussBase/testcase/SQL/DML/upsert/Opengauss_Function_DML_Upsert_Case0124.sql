-- @testpoint: upsert子查询表权限验证，没有权限，合理报错

--创建子查询表，插入数据
drop table if exists t_dml_upsert_sub0124;
create table t_dml_upsert_sub0124 (a int,b text);
insert into t_dml_upsert_sub0124 values(generate_series(1,10),'name'||generate_series(1,10));
--创建普通用户并切换至该用户
drop user if exists u_dml_upsert0124 cascade;
create user u_dml_upsert0124 password 'Test@123';
set session session authorization u_dml_upsert0124 password 'Test@123';
--普通用户没有子查询表的读权限
select * from t_dml_upsert_sub0124;
--普通用户创建upsert表并插入数据
drop table if exists t_dml_upsert0124;
create table t_dml_upsert0124 (a int primary key, b int, c int);
insert into t_dml_upsert0124 values (1,1,1),(2,2,2),(3,3,3),(4,4,4);
select * from t_dml_upsert0124;
--普通用户进行upsert子查询语句执行，报错没有权限
insert into t_dml_upsert0124 values(1,5) on duplicate key update b = (select min(a) from t_dml_upsert_sub0124 where a > excluded.b);
--进行普通用户子查询表读权限赋权
reset session authorization;
grant select on table t_dml_upsert_sub0124 to u_dml_upsert0124;
--普通用户进行upsert子查询语句执行，操作成功
set session session authorization u_dml_upsert0124 password 'Test@123';
select * from t_dml_upsert_sub0124;
--存在冲突
insert into t_dml_upsert0124 values(1,5) on duplicate key update b = (select min(a) from t_dml_upsert_sub0124 where a > excluded.b);
select * from t_dml_upsert0124;
--不存在冲突
insert into t_dml_upsert0124 values(5,5,5) on duplicate key update b = (select min(a) from t_dml_upsert_sub0124 where a > excluded.b);
select * from t_dml_upsert0124;
--处理测试数据
drop table if exists t_dml_upsert0124;
reset session authorization;
drop table if exists t_dml_upsert_sub0124;
drop user if exists u_dml_upsert0124 cascade;
