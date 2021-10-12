--  @testpoint:调用函数，只有一个参数，使用=>分隔符，将参数名和参数值隔开
drop FUNCTION if EXISTS func_add_sql012;
CREATE FUNCTION func_add_sql012(num1 integer) RETURN integer
AS
BEGIN
RETURN num1;
END;
/
--调用函数，使用=>分隔符，分隔参数名和参数值
CALL func_add_sql012(num1=>30);
drop FUNCTION func_add_sql012;