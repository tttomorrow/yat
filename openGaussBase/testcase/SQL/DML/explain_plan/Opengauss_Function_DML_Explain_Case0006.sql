-- @testpoint: explain plan语句结合where条件子查询使用
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t006;
drop table if exists explain_t006_bak;
create table explain_t006(a int, b int);
create table explain_t006_bak(f1 int,f2 int);
--使用explain plan语句，返回EXPLAIN SUCCESS
explain plan for select * from (select a from explain_t006 where b=(select f1 from explain_t006_bak));
explain plan for select a from explain_t006 where b=(select f1 from explain_t006_bak);
--查询PLAN_TABLE表信息,statement_id字段为空
select distinct object_name,statement_id from PLAN_TABLE where object_name = 'explain_t006' order by object_name;
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t006;
drop table explain_t006_bak;
