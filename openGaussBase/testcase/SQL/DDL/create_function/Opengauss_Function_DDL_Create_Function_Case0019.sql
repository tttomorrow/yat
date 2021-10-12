drop function if exists "func_test1*#"(integer, integer);
CREATE FUNCTION "func_test1*#"(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /
select proname from pg_proc where proname='func_test1*#';
call "func_test1*#"(999,1);
drop FUNCTION "func_test1*#";
