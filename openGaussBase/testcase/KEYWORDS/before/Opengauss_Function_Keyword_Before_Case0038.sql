-- @testpoint: 定义函数名为before
CREATE FUNCTION before(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select before (1,2);
drop function before;