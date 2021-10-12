-- @testpoint: pg_stat_reset_single_table_counters(oid)为当前数据库中的一个表或索引重置统计为0（需要系统管理员权限）。
-- 先清理环境
alter system set autovacuum to off;
drop table if exists sales;
select pg_stat_reset();
--创建表saless
CREATE TABLE sales
(prod_id NUMBER(6),
 cust_id NUMBER,
 time_id DATE,
 channel_id CHAR(1),
 promo_id NUMBER(6),
 quantity_sold NUMBER(3),
 amount_sold NUMBER(10,2)
);
-- testpoint:用表oid清除表相关的统计
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
SELECT pg_sleep(5);
select pg_stat_get_tuples_inserted(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_live_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_reset_single_table_counters(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_sleep(5);
select pg_stat_get_tuples_inserted(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_live_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
delete from sales where prod_id = 1;
select pg_sleep(5);
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_reset_single_table_counters(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_sleep(5);
select pg_stat_get_dead_tuples(a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_tuples_deleted(a.oid) from PG_CLASS a where a.relname = 'sales';
-- testpoint:用索引清除表相关的统计
create index index1 on sales(prod_id);
INSERT INTO sales VALUES(1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
select pg_sleep(5);
select pg_stat_get_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'index1';
select pg_stat_reset_single_table_counters(a.oid) from PG_CLASS a where a.relname = 'index1';
select pg_sleep(5);
select pg_stat_get_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'index1';
-- 环境恢复
drop table if exists sales;
alter system set autovacuum to on;