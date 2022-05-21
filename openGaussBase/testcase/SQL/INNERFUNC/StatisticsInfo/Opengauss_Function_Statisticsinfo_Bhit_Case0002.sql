-- @testpoint: pg_stat_get_blocks_hit(oid)函数的异常校验，合理报错
-- -- testpoint：空值、多参、少参、oid错误、超范围、表不存在
select pg_stat_get_blocks_hit('') from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_blocks_hit(a.oid,a.oid,a.oid) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_blocks_hit() from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_blocks_hit('&^%^&*') from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_blocks_hit(99999999999998789) from PG_CLASS a where a.relname = 'sales';
select pg_stat_get_blocks_hit(a.oid) from PG_CLASS a where a.relname = 'sales';