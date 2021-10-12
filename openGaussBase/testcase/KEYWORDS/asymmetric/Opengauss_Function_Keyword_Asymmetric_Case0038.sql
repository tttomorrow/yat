--  @testpoint:定义asymmetric为函数名,应该报错

CREATE FUNCTION asymmetric(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
select asymmetric (1,2);