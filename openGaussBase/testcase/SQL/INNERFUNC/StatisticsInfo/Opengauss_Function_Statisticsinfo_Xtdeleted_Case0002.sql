-- @testpoint: pg_stat_get_xact_tuples_deleted(oid)函数的异常校验，合理报错
select pg_stat_get_xact_tuples_deleted() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_deleted(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_deleted('') from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_deleted('**&&^') from PG_CLASS a where a.relname = 'sales';
