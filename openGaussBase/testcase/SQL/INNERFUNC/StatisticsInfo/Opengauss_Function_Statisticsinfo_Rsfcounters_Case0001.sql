-- @testpoint: pg_stat_reset_single_function_counters(oid)清除用在自定义函数上的所有统计信息函数的统计信息
alter system set autovacuum to off;
set track_functions to 'all';
set track_io_timing to 'on';
DROP FUNCTION IF EXISTS func_rsf;
CREATE FUNCTION func_rsf(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select func_rsf(3,7);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select 1, pg_stat_get_function_total_time(a.oid) from PG_PROC a where a.proname = 'func_rsf';
select 1, pg_stat_get_function_total_time(a.oid)<2 from PG_PROC a where a.proname = 'func_rsf';
-- 清除
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_reset_single_function_counters(a.oid) from PG_PROC a where a.proname = 'func_rsf';
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select 2, pg_stat_get_function_total_time(a.oid) from PG_PROC a where a.proname = 'func_rsf';
select 2, pg_stat_get_function_total_time(a.oid) is null from PG_PROC a where a.proname = 'func_rsf';
-- 再计数看是否会影响
select func_rsf(3,7);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select 3, pg_stat_get_function_total_time(a.oid) from PG_PROC a where a.proname = 'func_rsf';
select 3, pg_stat_get_function_total_time(a.oid)<2 from PG_PROC a where a.proname = 'func_rsf';
drop FUNCTION func_rsf;
set track_functions to 'none';
set track_io_timing to 'off';
alter system set autovacuum to on;