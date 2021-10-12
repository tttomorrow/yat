-- @testpoint: explain plan语句结合exists子查询嵌套case when的使用
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t010;
drop table if exists explain_t010_bak;
create table explain_t010(a int, b int);
create table explain_t010_bak(f1 int,f2 int);
--使用explain plan语句，返回EXPLAIN SUCCESS
explain plan for select t.a, (case when exists(select f1 from explain_t010_bak where f1 = 1) then 1 end) from explain_t010 t;
--查询PLAN_TABLE表信息,statement_id字段为空
select distinct object_name,statement_id from PLAN_TABLE where object_name = 'explain_t010' order by object_name;
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t010;
drop table explain_t010_bak;
