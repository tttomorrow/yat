-- @testpoint: 定义authorization为函数名
drop function if exists authorization;
CREATE FUNCTION authorization(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select authorization (1,2);
drop function if exists authorization;