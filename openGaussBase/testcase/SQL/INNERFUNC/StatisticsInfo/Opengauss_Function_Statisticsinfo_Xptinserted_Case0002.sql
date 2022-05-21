-- @testpoint: pg_stat_get_xact_partition_tuples_inserted(oid)函数的异常校验，合理报错
-- testpoint：空值、多参、少参、oid错误、超范围、表不存在
select pg_stat_get_xact_partition_tuples_inserted('') from pg_partition  a, pg_class b where a.relname = 'p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_xact_partition_tuples_inserted(a.oid,a.oid,a.oid) from pg_partition  a, pg_class b where a.relname = 'p2' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_xact_partition_tuples_inserted() from pg_partition  a, pg_class b where a.relname = 'sys_p1' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_xact_partition_tuples_inserted('&^%^&*') from pg_partition  a, pg_class b where a.relname = 'sys_p2' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_xact_partition_tuples_inserted(99999999999998789) from pg_partition  a, pg_class b where a.relname = 'sys_p2' and b.oid=a.parentid and b.relname='sales';
select pg_stat_get_xact_partition_tuples_inserted(a.oid) from pg_partition  a, pg_class b where a.relname = 'sys_p2' and b.oid=a.parentid and b.relname='sales';