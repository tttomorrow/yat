-- @testpoint: pg_stat_get_xact_tuples_inserted(oid)函数的异常校验，合理报错
select pg_stat_get_xact_tuples_inserted() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_inserted(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_inserted('') from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_inserted(9999999999999) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_tuples_inserted('**&&^') from PG_CLASS a where a.relname = 'sales';
