drop FUNCTION if EXISTS And_func1(integer, integer);
CREATE FUNCTION And_func1(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/

call  And_func1(999,1);
drop function And_func1;