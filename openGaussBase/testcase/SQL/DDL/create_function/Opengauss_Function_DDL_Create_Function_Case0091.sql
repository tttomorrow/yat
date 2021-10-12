--  @testpoint:创建函数指定参数IMMUTABLE
drop FUNCTION if exists func_add_sql005;
CREATE FUNCTION func_add_sql005(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
    /


call func_add_sql005(999,1);
drop FUNCTION func_add_sql005;