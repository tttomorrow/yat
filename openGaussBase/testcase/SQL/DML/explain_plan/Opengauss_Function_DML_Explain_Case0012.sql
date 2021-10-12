-- @testpoint: explain plan语句结合where条件的子查询减法运算
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t012;
drop table if exists explain_t012_bak;
create table explain_t012(a int, b int);
create table explain_t012_bak(f1 int,f2 int);
--使用explain plan语句，返回EXPLAIN SUCCESS
explain plan for select t.a  from explain_t012 t where t.a = (select f1 from explain_t012_bak) - 1;
--查询PLAN_TABLE表信息,statement_id字段为空
select distinct object_name,statement_id from PLAN_TABLE where object_name = 'explain_t012' order by object_name;
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t012;
drop table explain_t012_bak;