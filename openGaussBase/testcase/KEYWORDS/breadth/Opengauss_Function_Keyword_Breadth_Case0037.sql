--  @testpoint:定义breadth为函数名，应该报错
CREATE FUNCTION breadth(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
select breadth (1,2);