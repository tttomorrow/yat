-- @testpoint:explain plan语句结合merge语句和when matched update子句使用，合理报错
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t1;
drop table if exists explain_t2;
drop table if exists explain_t3;
create table explain_t1(a int, b int);
create table explain_t2(f1 int,f2 int);
create table explain_t3(f3 int,f4 int);
--使用explain plan语句，合理报错ERROR:  column "f1" does not exist
EXPLAIN PLAN FOR MERGE INTO explain_t1 USING explain_t2 ON (explain_t1.a = explain_t2.f1)
WHEN MATCHED THEN UPDATE SET b = (select f1 from explain_t1) WHERE explain_t2.f2 = (select f3 from explain_t3);
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t1;
drop table explain_t2;
drop table explain_t3;
