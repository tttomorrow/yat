--  @testpoint:创建函数指定参数STABLE
drop FUNCTION if exists func_add_sql006;
CREATE FUNCTION func_add_sql006(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    STABLE
    RETURNS NULL ON NULL INPUT;
/

call func_add_sql006(999,1);
drop FUNCTION func_add_sql006;