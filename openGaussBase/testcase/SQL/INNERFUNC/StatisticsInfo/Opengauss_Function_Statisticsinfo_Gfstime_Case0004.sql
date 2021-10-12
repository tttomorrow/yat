-- @testpoint: pg_stat_get_function_self_time(oid)函数的异常校验，合理报错
-- -- testpoint：空值、多参、少参、oid错误、超范围、表不存在
select pg_stat_get_function_self_time('')  from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_get_function_self_time(a.oid,a.oid,a.oid)  from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_get_function_self_time()  from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_get_function_self_time('&^%^&*')  from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_get_function_self_time(a.oid) from PG_PROC a where a.proname = 'func_add_sql';