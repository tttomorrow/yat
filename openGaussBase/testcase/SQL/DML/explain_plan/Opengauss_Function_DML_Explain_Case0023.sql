-- @testpoint: PLAN_TABLE进行insert操作，合理报错
--建表
drop table if exists explain_t23;
create table explain_t23(a int, b int);
--插入数据
insert into explain_t23 values(generate_series(1,500),generate_series(500,1000));
--使用EXPLAIN PLAN语句，返回EXPLAIN SUCCESS
explain plan set statement_id='TPCH-Q4' for select count(*) from explain_t23;
--查询PLAN_TABLE，标签信息也存储于PLAN_TABLE中
SELECT statement_id,operation FROM PLAN_TABLE;
--PLAN_TABLE使用insert语句，合理报错
insert into PLAN_TABLE(statement_id,operation,projection) values('TPCH-Q5',MAX,a);
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t23;