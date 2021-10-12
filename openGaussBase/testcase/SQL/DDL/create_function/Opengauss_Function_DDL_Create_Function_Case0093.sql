--  @testpoint:创建函数指定参数VOLATILE
drop FUNCTION if exists func_add_sql007;
CREATE FUNCTION func_add_sql007(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    VOLATILE
    RETURNS NULL ON NULL INPUT;
/

call func_add_sql007(999,1);
drop FUNCTION func_add_sql007;