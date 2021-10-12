--  @testpoint:函数名为空字符串，应该报错
CREATE FUNCTION ''(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/