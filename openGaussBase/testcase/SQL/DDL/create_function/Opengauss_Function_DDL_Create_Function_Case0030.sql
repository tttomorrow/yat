drop function if exists a_func1( func_15 integer, func_16 integer);
CREATE FUNCTION a_func1(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select proargnames from pg_proc where proname='a_func1';
call a_func1 (999,1);
drop FUNCTION a_func1;