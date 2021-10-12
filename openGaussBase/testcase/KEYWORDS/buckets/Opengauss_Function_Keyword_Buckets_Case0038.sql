--  @testpoint:定义buckets为函数名，应该报错
CREATE FUNCTION buckets(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
select buckets (1,2);