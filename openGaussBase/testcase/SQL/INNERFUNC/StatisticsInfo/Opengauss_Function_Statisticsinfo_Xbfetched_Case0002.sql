-- @testpoint: pg_stat_get_xact_blocks_fetched(oid)函数的异常校验，合理报错
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'sales1';
select pg_stat_get_xact_blocks_fetched(a.oid) from PG_CLASS a where a.relname = 'test_index3';
select pg_stat_get_xact_blocks_fetched() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_xact_blocks_fetched(99999999999999999) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_fetched('*&&^*') from PG_CLASS a where a.relname = 'test_index1';
