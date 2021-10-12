-- @testpoint: 使用CALL命令调用已定义的函数
drop function if exists func_add_sql;
CREATE FUNCTION func_add_sql(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/

CALL func_add_sql(1, 3);
drop function if exists func_add_sql;