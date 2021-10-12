-- @testpoint: 定义函数名为automapped
CREATE FUNCTION automapped(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
    /
select automapped (1,2);
drop function automapped;