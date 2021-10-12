drop function if exists "函数func1"(integer, integer);
CREATE FUNCTION "函数func1"(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /
select proname from pg_proc where proname='函数func1';
call "函数func1"(999,1);
drop FUNCTION "函数func1";