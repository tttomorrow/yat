drop function if exists func_15(integer, integer);
CREATE FUNCTION func_15(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /
select proname from pg_proc where proname='func_15';
drop FUNCTION func_15;