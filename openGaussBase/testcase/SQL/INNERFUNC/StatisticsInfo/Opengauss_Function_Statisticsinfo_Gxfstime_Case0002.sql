-- @testpoint: pg_stat_get_xact_function_self_time(oid)函数的异常校验，合理报错
	select pg_stat_get_xact_function_self_time() from PG_PROC a where a.proname = 'func02';
	select pg_stat_get_xact_function_self_time(a.oid,a.oid,a.oid)<2 from PG_PROC a where a.proname = 'func02';
    select pg_stat_get_xact_function_self_time('')<2 from PG_PROC a where a.proname = 'func02';
    select pg_stat_get_xact_function_self_time('*&^%$')<2 from PG_PROC a where a.proname = 'func02';