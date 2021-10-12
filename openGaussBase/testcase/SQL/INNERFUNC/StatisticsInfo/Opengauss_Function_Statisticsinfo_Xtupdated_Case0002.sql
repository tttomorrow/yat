-- @testpoint: pg_stat_get_xact_tuples_updated(oid)函数的异常校验，合理报错
select pg_stat_get_xact_tuples_updated() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_updated(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_updated('') from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_updated('**&&^') from PG_CLASS a where a.relname = 'sales';
