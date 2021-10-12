-- @testpoint: pg_stat_get_db_stat_reset_time(oid)上次重置数据库统计信息的时间。
alter system set autovacuum to off;
drop table if exists test;
CREATE TABLE test
     (
         sk            INTEGER               NOT NULL,
         grade              DECIMAL(5,2)
     );
create index test_index on test (sk);
--    1.调用函数pg_stat_reset
select pg_stat_reset();
SELECT pg_sleep(1);
select  pg_stat_get_db_stat_reset_time(a.oid)  between current_timestamp-0.00002 and current_timestamp from PG_DATABASE a where a.datname = CURRENT_CATALOG;
--    2.对表或索引操作pg_stat_reset_single_table_counters
select  pg_stat_reset_single_table_counters(a.oid) from PG_CLASS a where a.relname = 'test_index';
SELECT pg_sleep(1);
select  pg_stat_get_db_stat_reset_time(a.oid)  between current_timestamp-0.00002 and current_timestamp from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select  pg_stat_reset_single_table_counters(a.oid)from PG_CLASS a where a.relname = 'test';
SELECT pg_sleep(1);
select  pg_stat_get_db_stat_reset_time(a.oid)  between current_timestamp-0.00002 and current_timestamp from PG_DATABASE a where a.datname = CURRENT_CATALOG;
drop table if exists test;
alter system set autovacuum to on;