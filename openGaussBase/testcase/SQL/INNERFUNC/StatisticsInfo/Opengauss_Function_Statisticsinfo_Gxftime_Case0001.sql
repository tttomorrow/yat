-- @testpoint: pg_stat_get_xact_function_total_time(oid)获取当前事务中该函数所花费的总挂钟时间（以微秒为单位），包括花费在此函数调用上的时间。
alter system set autovacuum to off;
begin;
/
set track_functions to 'all';
set track_io_timing to 'on';
-- 内建函数 不适用
SELECT pg_column_size(1);
SELECT pg_sleep(10);
select pg_stat_get_xact_function_total_time(a.oid) is null from PG_PROC a where a.proname = 'pg_column_size';
-- 自定义函数
DROP FUNCTION IF EXISTS func_add_sql;
CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
AS 'select $1 + $2;'
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT;
/
select func_add_sql(3,7);
SELECT pg_sleep(10);
select pg_stat_get_xact_function_total_time(a.oid)<2 from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_get_xact_function_total_time(a.oid)=2 from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_reset();
select func_add_sql(3,7);
SELECT pg_sleep(10);
select pg_stat_get_xact_function_total_time(a.oid)<2 from PG_PROC a where a.proname = 'func_add_sql';
select pg_stat_get_xact_function_total_time(a.oid)=2 from PG_PROC a where a.proname = 'func_add_sql';
drop FUNCTION func_add_sql;
-- 过程语言函数
DROP TABLE IF EXISTS integertable;
DROP PROCEDURE IF EXISTS proc_while_loop;
CREATE TABLE integertable(c1 integer);
CREATE OR REPLACE PROCEDURE proc_while_loop(maxval in integer)
AS
    DECLARE
    i int :=1;
    BEGIN
        WHILE i < maxval LOOP
            INSERT INTO integertable VALUES(i);
            i:=i+1;
        END LOOP;
	EXECUTE 'select pg_sleep(2)';
    END;
/
CALL proc_while_loop(10);
SELECT pg_sleep(10);
select pg_stat_get_xact_function_total_time(a.oid)>1 from PG_PROC a where a.proname = 'proc_while_loop';
select pg_stat_get_xact_function_total_time(a.oid)=1 from PG_PROC a where a.proname = 'proc_while_loop';
DROP PROCEDURE proc_while_loop;
DROP TABLE integertable;
set track_functions to 'none';
set track_io_timing to 'off';
end;
alter system set autovacuum to on;