--  @testpoint:创建函数，添加参数LEAKPROOF
drop FUNCTION if exists func_add_sql100;
CREATE FUNCTION func_add_sql100(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    VOLATILE
    not SHIPPABLE
     LEAKPROOF
    RETURNS NULL ON NULL INPUT;
/


call func_add_sql100(999,1);
drop FUNCTION func_add_sql100;