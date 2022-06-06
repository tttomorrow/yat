-- @testpoint: pg_stat_get_function_total_time(oid)函数的异常校验，合理报错
select pg_stat_get_function_total_time('') from PG_PROC a where proname = 'pg_stat_reset';
select pg_stat_get_function_total_time() from PG_PROC a where proname = 'pg_stat_reset';
select pg_stat_get_function_total_time(a.oid,a.oid,a.oid) from PG_PROC a where proname = 'pg_stat_reset';
select pg_stat_get_function_total_time(9999999999999) from PG_PROC a where proname = 'pg_stat_reset';
select pg_stat_get_function_total_time('*&^%$') from PG_PROC a where proname = 'pg_stat_reset';