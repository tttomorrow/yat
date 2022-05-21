-- @testpoint: pg_stat_get_db_xact_rollback(oid)函数的异常校验，合理报错
select pg_stat_get_db_xact_rollback('') from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_xact_rollback() from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_xact_rollback(a.oid,a.oid,a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_xact_rollback(9999999999999) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_xact_rollback('*&^%$') from PG_DATABASE a where a.datname = CURRENT_CATALOG;