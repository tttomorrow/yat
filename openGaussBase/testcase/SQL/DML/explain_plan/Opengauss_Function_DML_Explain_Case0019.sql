-- @testpoint: explain plan语句结合merge语句和when matched中using子句使用
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t019;
drop table if exists explain_t019_bak;
drop table if exists explain_t019_bak1;
create table explain_t019(a int, b int);
create table explain_t019_bak(f1 int,f2 int);
create table explain_t019_bak1(f3 int,f4 int);
--使用explain plan语句，返回EXPLAIN SUCCESS
explain plan for merge into explain_t019 using (select * from explain_t019_bak where f1 = (select f3 from explain_t019_bak1)) tt2 on (explain_t019.a = tt2.f1)
when matched then update set b = tt2.f2 + 1 where tt2.f2 = 2;
--查询PLAN_TABLE表信息,statement_id字段为空
select distinct object_name,statement_id from PLAN_TABLE where object_name = 'explain_t019' order by object_name;
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t019;
drop table explain_t019_bak;
drop table explain_t019_bak1;