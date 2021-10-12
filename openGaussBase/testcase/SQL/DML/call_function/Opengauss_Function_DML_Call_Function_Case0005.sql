-- @testpoint: 调用函数，不加函数名，合理报错
drop FUNCTION if EXISTS func_add_sql006;
CREATE FUNCTION func_add_sql006(num1 integer, num2 integer) RETURN integer
AS
BEGIN
RETURN num1 + num2;
END;
/

CALL (1, 3);
drop FUNCTION func_add_sql006;