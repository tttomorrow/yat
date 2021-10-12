--  @testpoint:创建函数，添加参数NOT LEAKPROOF
drop FUNCTION if exists func_add_sql101;
CREATE FUNCTION func_add_sql101(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    VOLATILE
    not SHIPPABLE
    NOT LEAKPROOF
    RETURNS NULL ON NULL INPUT;
/


call func_add_sql101(999,1);
drop FUNCTION func_add_sql101;