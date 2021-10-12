-- @testpoint: pg_stat_get_tuples_inserted(oid)函数的异常校验，合理报错
drop table if exists sales;
--创建表sales
CREATE TABLE sales
(prod_id NUMBER(6),
 time_id DATE
);
-- 数据插入
INSERT INTO sales VALUES(1, '2019-01-10 00:00:00');
select pg_stat_get_tuples_inserted() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_inserted(a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
drop table sales cascade;