--  @testpoint:定义by为函数名
CREATE FUNCTION by(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
select by (1,2);