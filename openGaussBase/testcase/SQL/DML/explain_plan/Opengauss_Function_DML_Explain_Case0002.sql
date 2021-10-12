-- @testpoint:explain plan语句结合not in子查询使用
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t1;
drop table if exists explain_t2;
create table explain_t1(a int, b int);
create table explain_t2(f1 int,f2 int);
--使用explain plan语句，返回EXPLAIN SUCCESS
explain plan for select a from explain_t1 where a in (select f1 from explain_t2);
--查询PLAN_TABLE表信息,statement_id字段为空
select statement_id,object_name,options from PLAN_TABLE where object_name in('explain_t1','explain_t2');
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t1;
drop table explain_t2;