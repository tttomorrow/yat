-- @testpoint: explain plan语句结合update语句中的子查询使用
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t016;
drop table if exists explain_t016_bak;
create table explain_t016(a int, b int);
create table explain_t016_bak(f1 int,f2 int);
--使用explain plan语句，返回EXPLAIN SUCCESS
explain plan for update explain_t016 set a = 1 where b = (select f1 from explain_t016_bak where f1 = 1);
--查询PLAN_TABLE表信息,statement_id字段为空
select distinct object_name,statement_id from PLAN_TABLE where object_name = 'explain_t016' order by object_name;
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t016;
drop table explain_t016_bak;
