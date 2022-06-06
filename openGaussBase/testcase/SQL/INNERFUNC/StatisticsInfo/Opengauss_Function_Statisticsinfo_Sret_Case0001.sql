-- @testpoint: pg_stat_reset()为当前数据库重置统计计数器为0（需要系统管理员权限）。
alter system set autovacuum to off;
set track_functions to 'all';
set track_io_timing to 'on';
DROP FUNCTION IF EXISTS func_add_sql;
CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
AS 'select $1 + $2;'
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT;
/
select func_add_sql(3,7);
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_function_total_time(a.oid)<2 from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset();
SELECT pg_sleep(6);
SELECT pg_sleep(6);
select pg_stat_get_function_total_time(a.oid) is null from PG_PROC a where a.proname = 'func_add_sql';
drop FUNCTION func_add_sql;
set track_functions to 'none';
set track_io_timing to 'off';
alter system set autovacuum to on;