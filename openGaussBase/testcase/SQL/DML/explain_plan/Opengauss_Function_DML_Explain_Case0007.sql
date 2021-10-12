-- @testpoint: explain plan语句结合in子查询和exists的嵌套使用
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t007;
drop table if exists explain_t007_bak;
drop table if exists explain_t007_bak_1;
create table explain_t007(a int, b int);
create table explain_t007_bak(f1 int,f2 int);
create table explain_t007_bak_1(f3 int,f4 int);
--使用explain plan语句，返回EXPLAIN SUCCESS
explain plan for select * from explain_t007 where exists(select f1 from explain_t007_bak GROUP BY f1 HAVING f1 IN (select f3 from explain_t007_bak_1));
--查询PLAN_TABLE表信息,statement_id字段为空
select distinct object_name,statement_id from PLAN_TABLE where object_name = 'explain_t007' order by object_name;
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t007;
drop table explain_t007_bak;
drop table explain_t007_bak_1;
