-- @testpoint: 定义函数名为backward
CREATE FUNCTION backward(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select backward (1,2);
drop function backward;