-- @testpoint: explain plan语句结合where条件子查询和表的子查询使用
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t005;
drop table if exists explain_t005_bak;
drop table if exists explain_t005_bak1;
create table explain_t005(a int, b int);
create table explain_t005_bak(f1 int,f2 int);
create table explain_t005_bak1(f3 int,f4 int);
--使用explain plan语句，返回EXPLAIN SUCCESS
explain plan for select a from explain_t005 where exists(select * from explain_t005_bak) group by a having a in (select f3 from explain_t005_bak1);
--查询PLAN_TABLE表信息,statement_id字段为空
select distinct object_name,statement_id from PLAN_TABLE where object_name = 'explain_t005' order by object_name;
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t005;
drop table explain_t005_bak;
drop table explain_t005_bak1;

