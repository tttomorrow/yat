--  @testpoint:创建函数加SHIPPABLE参数
drop FUNCTION if exists func_add_sql008;
CREATE FUNCTION func_add_sql008(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    VOLATILE
    SHIPPABLE
    RETURNS NULL ON NULL INPUT;
/


call func_add_sql008(999,1);
drop FUNCTION func_add_sql008;