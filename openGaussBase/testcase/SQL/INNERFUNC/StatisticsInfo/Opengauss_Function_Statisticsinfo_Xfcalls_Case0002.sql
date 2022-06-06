-- @testpoint: pg_stat_get_xact_function_calls(oid)函数的异常校验，合理报错
select pg_stat_get_xact_function_calls() from PG_PROC b where proname = 'pg_stat_get_tuples_inserted';
select pg_stat_get_xact_function_calls(b.oid,b.oid,b.oid) from PG_PROC b where proname = 'pg_stat_get_tuples_inserted';
select pg_stat_get_xact_function_calls('*&^%') from PG_PROC b where b.proname = 'pg_stat_get_tuples_inserted';
select pg_stat_get_xact_function_calls(98765412345678) from PG_PROC b where proname = 'pg_stat_get_tuples_inserted';