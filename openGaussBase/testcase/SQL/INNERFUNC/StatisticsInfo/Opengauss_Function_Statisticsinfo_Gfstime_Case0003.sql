-- @testpoint: pg_stat_get_function_self_time(oid)返回某函数本身的执行时间，不包括调用其它函数所花费的时间。
-- 开启统计开关
alter system set autovacuum to off;
set track_functions to 'all';
set track_io_timing to 'on';
-- 清理统计计数
select pg_stat_reset();
-- testpoint1: 未调用其它函数的结果和pg_stat_get_function_total_time一样
drop function if exists func_add_sql;
CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
AS 'select $1 + $2;'
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT;
/
select func_add_sql(3,7);
SELECT pg_sleep(2);
select pg_stat_get_function_self_time(a.oid)=pg_stat_get_function_total_time(a.oid) from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset();
select func_add_sql(3,7);
SELECT pg_sleep(2);
select pg_stat_get_function_self_time(a.oid)<2,pg_stat_get_function_total_time(a.oid)<2 from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_get_function_self_time(a.oid)=2,pg_stat_get_function_total_time(a.oid)=2 from PG_PROC a where a.proname = 'func_add_sql';

-- testpoint2：函数内调用了其它函数，其里被调用的函数的时间不计
drop function if exists func01;
drop function if exists func02;
create or replace function func01()returns void as $$
begin
    raise notice ' from func01(): hello PG';
end ;
$$language plpgsql;
/
create or replace function func02() returns void as $$
begin
    perform  func01();
end;
$$language plpgsql;
/
select  func02();
SELECT pg_sleep(2);
-- 小于整体的时间
select pg_stat_get_function_self_time(a.oid)<pg_stat_get_function_total_time(a.oid) from PG_PROC a where a.proname = 'func02';
select pg_stat_get_function_self_time(a.oid)<2 from PG_PROC a where a.proname = 'func02';
select pg_stat_get_function_self_time(a.oid)=2 from PG_PROC a where a.proname = 'func02';
-- 恢复环境
drop function func01;
drop function func02;
drop FUNCTION func_add_sql;
set track_functions to 'none';
set track_io_timing to 'off';
alter system set autovacuum to on;