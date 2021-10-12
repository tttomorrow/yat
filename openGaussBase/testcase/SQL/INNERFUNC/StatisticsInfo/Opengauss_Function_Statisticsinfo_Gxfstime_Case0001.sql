-- @testpoint: pg_stat_get_xact_function_self_time(oid)在当前事务中仅花费在此功能上的时间，不包括花费在调用函数上的时间。
alter system set autovacuum to off;
set track_functions to 'all';
set track_io_timing to 'on';
-- 未调用其它函数的结果和pg_stat_get_xact_function_total_time一样
begin;
/
drop function if exists func_add_sql;
CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
AS 'select $1 + $2;'
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT;
/
select func_add_sql(3,7);
SELECT pg_sleep(2);
select pg_stat_get_xact_function_self_time(a.oid)=pg_stat_get_xact_function_total_time(a.oid) from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset();
select func_add_sql(3,7);
SELECT pg_sleep(2);
select pg_stat_get_xact_function_self_time(a.oid)<2,pg_stat_get_xact_function_total_time(a.oid)<2 from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_get_xact_function_self_time(a.oid)=2,pg_stat_get_xact_function_total_time(a.oid)<2 from PG_PROC a where a.proname = 'func_add_sql';
drop FUNCTION func_add_sql;
end;
-- 函数内调用了其它函数
begin;
/
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
SELECT pg_sleep(3);
select pg_stat_get_xact_function_self_time(a.oid)<pg_stat_get_xact_function_total_time(a.oid) from PG_PROC a where a.proname = 'func02';
select pg_stat_get_xact_function_self_time(a.oid)<2 from PG_PROC a where a.proname = 'func02';
select pg_stat_get_xact_function_self_time(a.oid)=2 from PG_PROC a where a.proname = 'func02';
drop function func01;
drop function func02;
end;
-- 恢复环境
set track_functions to 'none';
set track_io_timing to 'off';
alter system set autovacuum to on;