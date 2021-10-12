--  @testpoint:调用函数，函数名不正确，合理报错
drop FUNCTION if EXISTS func_add_sql004;
CREATE FUNCTION func_add_sql004(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/
--函数名不正确，合理报错
CALL func_add_sql005(1, 3);
drop FUNCTION func_add_sql004;