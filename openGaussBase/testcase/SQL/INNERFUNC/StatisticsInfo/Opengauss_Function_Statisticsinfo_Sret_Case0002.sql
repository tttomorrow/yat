-- @testpoint: pg_stat_reset()函数的异常校验，合理报错
-- 多参
    select pg_stat_reset('*&^%');
    select pg_stat_reset(61888);
