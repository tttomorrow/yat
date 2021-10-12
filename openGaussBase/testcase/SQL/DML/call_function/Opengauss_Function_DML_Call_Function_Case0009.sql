--  @testpoint:调用函数，使用=>分隔符，将参数名和参数值隔开，任意顺序排列
drop FUNCTION if EXISTS func_add_sql010;
CREATE FUNCTION func_add_sql010(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/
--调用函数，参数任意顺序排列
CALL func_add_sql010(num2=>10, num1=>30);
drop FUNCTION func_add_sql010;