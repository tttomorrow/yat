-- @testpoint: pg_stat_get_db_tuples_returned(oid)函数的异常校验，合理报错
-- testpoint：oid错误、多参、少参、特殊字符
-- 开发确认oid不存在时返回结果是0
select pg_stat_get_db_tuples_returned(999999);
select pg_stat_get_db_tuples_returned(a.oid,a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_returned() from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_returned('&^%%^') from PG_DATABASE a where a.datname = CURRENT_CATALOG;