-- @testpoint: pg_stat_get_xact_blocks_hit(oid)函数的异常校验，合理报错
select pg_stat_get_xact_blocks_hit(a.oid) from PG_CLASS a where a.relname = 'sales1';
select pg_stat_get_xact_blocks_hit(a.oid) from PG_CLASS a where a.relname = 'test_index3';
select pg_stat_get_xact_blocks_hit() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_hit(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'test_index1';
select pg_stat_get_xact_blocks_hit(99999999999999999) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_xact_blocks_hit('*&&^*') from PG_CLASS a where a.relname = 'test_index1';
