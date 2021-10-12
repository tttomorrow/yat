-- @testpoint: pg_stat_get_db_stat_reset_time(oid)函数的异常校验，合理报错
-- 调用函数pg_stat_reset重置，给空值、特殊字符（oid不存在）
    select pg_stat_reset();
    select pg_stat_get_db_stat_reset_time('*&^%');
    select pg_stat_get_db_stat_reset_time();
