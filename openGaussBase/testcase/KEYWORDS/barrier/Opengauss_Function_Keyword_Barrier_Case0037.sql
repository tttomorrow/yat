-- @testpoint: 定义函数名为barrier
CREATE FUNCTION barrier(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select barrier (1,2);
drop function barrier;