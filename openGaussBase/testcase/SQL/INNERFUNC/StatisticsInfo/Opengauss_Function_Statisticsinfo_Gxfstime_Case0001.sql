-- @testpoint: pg_stat_get_xact_function_self_time(oid)在当前事务中仅花费在此功能上的时间，不包括花费在调用函数上的时间。
--step1:设置参数;expect:成功
alter system set autovacuum to off;
set track_functions to 'all';
set track_io_timing to 'on';
--step2:未调用其它函数的结果和pg_stat_get_xact_function_total_time一样;expect:成功
begin;
/
drop function if exists func_add_sql;
create function func_add_sql(integer, integer) returns integer
as 'select $1 + $2;'
language sql
immutable
returns null on null input;
/
select func_add_sql(3,7);
select pg_sleep(6);
select pg_sleep(6);
select pg_stat_get_xact_function_self_time(a.oid)=pg_stat_get_xact_function_total_time(a.oid) from pg_proc a where a.proname = 'func_add_sql';
select pg_stat_reset();
select func_add_sql(3,7);
select pg_sleep(6);
select pg_sleep(6);
select pg_stat_get_xact_function_self_time(a.oid)<2,pg_stat_get_xact_function_total_time(a.oid)<2 from pg_proc a where a.proname = 'func_add_sql';
select pg_sleep(6);
select pg_sleep(6);
select pg_stat_get_xact_function_self_time(a.oid)=2,pg_stat_get_xact_function_total_time(a.oid)<2 from pg_proc a where a.proname = 'func_add_sql';
drop function func_add_sql;
end;
--step3:函数内调用了其它函数;expect:成功
begin;
/
drop function if exists func01;
drop function if exists func02;
create or replace function func01()returns void as $$
begin
    raise notice ' from func01(): hello pg';
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
select pg_sleep(6);
select pg_sleep(6);
select pg_stat_get_xact_function_self_time(a.oid)<pg_stat_get_xact_function_total_time(a.oid) from pg_proc a where a.proname = 'func02';
select pg_sleep(6);
select pg_sleep(6);
select pg_stat_get_xact_function_self_time(a.oid)<2 from pg_proc a where a.proname = 'func02';
select pg_sleep(6);
select pg_sleep(6);
select pg_stat_get_xact_function_self_time(a.oid)=2 from pg_proc a where a.proname = 'func02';
drop function func01;
drop function func02;
end;
--step4:恢复环境;expect:成功
set track_functions to 'none';
set track_io_timing to 'off';
alter system set autovacuum to on;