-- @testpoint: 调用函数，使用参数值:=参数名，按顺序传递，合理报错

drop FUNCTION if EXISTS func_add_sql015;
CREATE FUNCTION func_add_sql015(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/
--调用函数，使用参数值:=参数名，按参数按顺序传递
CALL func_add_sql015(1:=num1 , 3:=num2);
drop FUNCTION func_add_sql015;