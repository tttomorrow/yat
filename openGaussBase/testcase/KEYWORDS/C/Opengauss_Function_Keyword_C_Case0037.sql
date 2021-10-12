-- @testpoint: 定义C为函数名
CREATE FUNCTION C(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/    
select C (1,2);
drop function C;