-- @testpoint: 定义函数名为bigint
CREATE or replace FUNCTION begint(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
drop function begint;