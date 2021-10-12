-- @testpoint: 定义函数名为begin_non_anoyblock
CREATE FUNCTION begin_non_anoyblock(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select begin_non_anoyblock (1,2);
drop function begin_non_anoyblock;