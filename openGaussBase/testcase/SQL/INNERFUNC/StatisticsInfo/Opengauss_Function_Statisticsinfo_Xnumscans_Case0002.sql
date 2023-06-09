-- @testpoint: pg_stat_get_xact_numscans(oid)函数的异常校验，合理报错
select pg_stat_get_xact_numscans('') from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans(9999999999999) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_numscans('*&^%$') from PG_CLASS a where a.relname = 'sales';