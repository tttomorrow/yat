-- @testpoint: 定义atomic为函数名
CREATE or replace FUNCTION atomic(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select atomic (1,2);
drop function atomic;