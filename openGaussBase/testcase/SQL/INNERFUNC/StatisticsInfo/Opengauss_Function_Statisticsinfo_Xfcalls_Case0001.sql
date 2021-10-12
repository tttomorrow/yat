-- @testpoint: pg_stat_get_xact_function_calls(oid)返回在当前事务中调用某函数的次数
alter system set autovacuum to off;
begin;
/
-- 自定义函数
set track_functions to 'all';
set track_io_timing to 'on';
DROP FUNCTION IF EXISTS func_add_sql;
CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer AS 'select $1 + $2;' LANGUAGE SQL IMMUTABLE RETURNS NULL ON NULL INPUT;
/
select func_add_sql(3,7);
SELECT pg_sleep(1);
select pg_stat_get_xact_function_calls(a.oid) from PG_PROC a where a.proname = 'func_add_sql';
select func_add_sql(3,7);
select func_add_sql(8,9);
SELECT pg_sleep(1);
select pg_stat_get_xact_function_calls(a.oid) from PG_PROC a where a.proname = 'func_add_sql';
set track_functions to 'none';
set track_io_timing to 'off';
select pg_stat_get_xact_function_calls(a.oid) from PG_PROC a where a.proname = 'func_add_sql';
drop FUNCTION func_add_sql;
select pg_stat_get_xact_function_calls(a.oid)  from PG_PROC a where a.proname = 'func_add_sql';
-- 过程函数
set track_functions to 'all';
set track_io_timing to 'on';
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
    END;
/
CALL proc_while_loop(10);
SELECT pg_sleep(1);
select pg_stat_get_xact_function_calls(a.oid) from PG_PROC a where a.proname = 'proc_while_loop';
CALL proc_while_loop(10);
CALL proc_while_loop(10);
SELECT pg_sleep(1);
select pg_stat_get_xact_function_calls(a.oid) from PG_PROC a where a.proname = 'proc_while_loop';
set track_functions to 'none';
set track_io_timing to 'off';
select pg_stat_get_xact_function_calls(a.oid) from PG_PROC a where a.proname = 'proc_while_loop';
DROP PROCEDURE proc_while_loop;
DROP TABLE integertable;
select pg_stat_get_xact_function_calls(a.oid) from PG_PROC a where a.proname = 'proc_while_loop';
end;
alter system set autovacuum to on;