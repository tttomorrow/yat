--  @testpoint:创建函数加NOT SHIPPABLE参数
drop FUNCTION if exists func_add_sql009;
CREATE FUNCTION func_add_sql009(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    VOLATILE
    not SHIPPABLE
    RETURNS NULL ON NULL INPUT;
/


call func_add_sql009(999,1);
drop FUNCTION func_add_sql009;