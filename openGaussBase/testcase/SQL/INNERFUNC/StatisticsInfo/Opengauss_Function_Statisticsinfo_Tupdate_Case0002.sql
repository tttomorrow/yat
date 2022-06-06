-- @testpoint: pg_stat_get_partition_tuples_updated(oid)函数的异常校验，合理报错
drop table if exists sales;
--创建表sales
CREATE TABLE sales
(prod_id NUMBER(6),
 time_id DATE
);
-- 数据插入、更新
INSERT INTO sales VALUES(1, '2019-01-10 00:00:00');
update sales set time_id = '2017-12-10 00:00:00' where prod_id = 1;
select pg_stat_get_tuples_updated() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_updated(a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_updated(98765432198765);
drop table sales cascade;