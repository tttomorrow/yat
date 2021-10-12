-- @testpoint: 定义verbose是函数名
CREATE FUNCTION verbose(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;


    select  verbose(1,2);
	
drop function if exists verbose;