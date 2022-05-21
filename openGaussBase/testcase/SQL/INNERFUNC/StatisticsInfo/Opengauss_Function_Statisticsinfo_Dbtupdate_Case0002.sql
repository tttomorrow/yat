-- @testpoint: pg_stat_get_db_tuples_updated(oid)函数的异常校验，合理报错
select pg_stat_get_db_tuples_updated('') from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_updated() from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_updated(a.oid,a.oid,a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_updated(98765432112345) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_updated('*&^%$') from PG_DATABASE a where a.datname = CURRENT_CATALOG;
