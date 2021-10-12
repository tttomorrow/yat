-- @testpoint: pg_stat_get_xact_function_total_time(oid)函数的异常校验，合理报错
select pg_stat_get_xact_function_total_time() is null from PG_PROC a where a.proname = 'pg_column_size';
select pg_stat_get_xact_function_total_time('') is null from PG_PROC a where a.proname = 'pg_column_size';
select pg_stat_get_xact_function_total_time(a.oid,a.oid) is null from PG_PROC a where a.proname = 'pg_column_size';
select pg_stat_get_xact_function_total_time('*&^^&*') is null from PG_PROC a where a.proname = 'pg_column_size';