-- @testpoint: pg_stat_reset_single_table_counters(oid)函数的异常校验，合理报错
-- testpoint：空值、多参、少参、oid错误、超范围、表不存在
select pg_stat_reset_single_table_counters('') from PG_CLASS a where a.relname = 'sales';
select pg_stat_reset_single_table_counters(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_reset_single_table_counters() from PG_PARTITION a where a.relname = 'sys_p1';
select pg_stat_reset_single_table_counters('&^%^&*') from PG_CLASS a where a.relname = 'sales';
select pg_stat_reset_single_table_counters(99999999999998789) from PG_CLASS a where a.relname = 'sales';
select pg_stat_reset_single_table_counters(a.oid) from PG_CLASS a where a.relname = 'sales';
