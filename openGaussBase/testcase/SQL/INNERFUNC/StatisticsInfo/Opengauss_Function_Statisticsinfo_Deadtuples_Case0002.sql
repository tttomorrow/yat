-- @testpoint: pg_stat_get_dead_tuples(oid)函数的异常校验，合理报错
drop table if exists sales;
--创建表sales
CREATE TABLE sales
(prod_id NUMBER(6),
 time_id DATE
);
-- 数据插入
INSERT INTO sales VALUES(1, '2019-01-10 00:00:00');
delete from sales where prod_id = 1;
select pg_stat_get_dead_tuples() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_dead_tuples(a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_dead_tuples(98765432198765);
select pg_stat_get_dead_tuples('*&^%^&*');
drop table sales cascade;