--  @testpoint:不带schema，按参数值传递,调用函数
drop FUNCTION if EXISTS func_add_sql001;
CREATE FUNCTION func_add_sql001(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/

CALL func_add_sql001(1, 3);
drop FUNCTION func_add_sql001;