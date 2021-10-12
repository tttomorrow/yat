--  @testpoint:创建函数，参数模式放在参数名前面,函数创建成功
drop FUNCTION if exists func_add_sqlf;
CREATE FUNCTION func_add_sqlf(INOUT integer, IN integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE sql
    RETURNS NULL ON NULL INPUT;
    /
    call func_add_sqlf(999,1);
    drop FUNCTION func_add_sqlf;