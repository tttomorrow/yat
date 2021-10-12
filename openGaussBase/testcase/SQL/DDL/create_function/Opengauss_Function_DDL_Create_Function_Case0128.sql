drop FUNCTION if exists func_add_sqld;
CREATE FUNCTION func_add_sqld(integer, integer) RETURNS integer DETERMINISTIC
    AS 'select $1 + $2;'
    LANGUAGE SQL
    STABLE
    RETURNS NULL ON NULL INPUT;
/

call func_add_sqld(999,1);
drop FUNCTION func_add_sqld;