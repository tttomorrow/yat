-- @testpoint: PLAN_TABLE进行update操作，合理报错
--建表
drop table if exists explain_t24;
create table explain_t24(a int, b int);
--插入数据
insert into explain_t24 values(generate_series(1,500),generate_series(500,1000));
--使用EXPLAIN PLAN语句，返回EXPLAIN SUCCESS
explain plan set statement_id='TPCH-Q4' for select count(*) from explain_t24;
--查询PLAN_TABLE，标签信息也存储于PLAN_TABLE中
SELECT statement_id,operation FROM PLAN_TABLE;
--PLAN_TABLE使用update语句，合理报错ERROR:  cannot update view "plan_table"
update PLAN_TABLE set statement_id = 'TPCH-Q5' where operation = 'AGGREGATE';
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t24;