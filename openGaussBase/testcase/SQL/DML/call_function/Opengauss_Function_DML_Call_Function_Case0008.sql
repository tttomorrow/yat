--  @testpoint:调用函数，使用=>分隔符，将参数名和参数值隔开，按顺序传递
drop FUNCTION if EXISTS func_add_sql009;
CREATE FUNCTION func_add_sql009(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/
--调用函数，参数按顺序传递
CALL func_add_sql009(num1=>1, num2=>3);
drop FUNCTION func_add_sql009;