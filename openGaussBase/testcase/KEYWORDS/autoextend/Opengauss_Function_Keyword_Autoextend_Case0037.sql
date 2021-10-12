-- @testpoint: 列名为autoextend ，并且定义autoextend 列default值
CREATE FUNCTION autoextend(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
    /
select autoextend (1,2);
drop function autoextend;