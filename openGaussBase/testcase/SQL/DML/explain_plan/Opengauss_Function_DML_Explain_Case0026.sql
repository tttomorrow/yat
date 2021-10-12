-- @testpoint: 清理PLAN_TABLE表中的数据
--建表
drop table if exists explain_t26;
create table explain_t26(a int, b int);
--插入数据
insert into explain_t26 values(generate_series(1,500),generate_series(500,1000));
--使用EXPLAIN PLAN语句，返回EXPLAIN SUCCESS
explain plan set statement_id='TPCH-Q4' for select count(*) from explain_t26;
--查询PLAN_TABLE，标签信息也存储于PLAN_TABLE中
SELECT statement_id,operation FROM PLAN_TABLE;
--清理PLAN_TABLE数据
DELETE FROM PLAN_TABLE;
--删表
drop table explain_t26;