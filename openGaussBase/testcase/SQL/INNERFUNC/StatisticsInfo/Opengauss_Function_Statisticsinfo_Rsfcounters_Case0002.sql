-- @testpoint: pg_stat_reset_single_function_counters(oid)函数的异常校验，合理报错
select pg_stat_reset_single_function_counters('') from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset_single_function_counters() from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset_single_function_counters(a.oid,a.oid,a.oid) from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset_single_function_counters(99999999999999999) from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset_single_function_counters('*&^%%*^$') from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset_single_function_counters(a.oid) from PG_PROC a where a.proname = 'func_add_sql';