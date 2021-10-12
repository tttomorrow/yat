-- @testpoint: 定义at为函数名
CREATE FUNCTION at(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
    /
select at (1,2);
drop function at;