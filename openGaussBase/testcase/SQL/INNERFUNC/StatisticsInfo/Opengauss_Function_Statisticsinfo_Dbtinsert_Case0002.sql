-- @testpoint: pg_stat_get_db_tuples_inserted(oid)函数的异常校验，合理报错
select pg_stat_get_db_tuples_inserted('') from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_inserted() from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_inserted(a.oid,a.oid,a.oid) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_inserted(98766532345678999764) from PG_DATABASE a where a.datname = CURRENT_CATALOG;
select pg_stat_get_db_tuples_inserted('*&^545678*&^%') from PG_DATABASE a where a.datname = CURRENT_CATALOG;
